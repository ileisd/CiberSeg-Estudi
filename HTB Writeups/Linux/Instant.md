<p align="center">
  <img src="https://github.com/user-attachments/assets/bb633264-4148-4237-9b21-f4a37268670a" alt="instant-htb-header" width="50%" height="50%">
</p>

---

## NMAP Scanning
Escaneig a través d'enviament de paquets TCP SYN a tots els ports del host per detectar quins estan oberts.
````bash
> nmap -p- --open -sS -v -n --min-rate=5000 -Pn -n 10.10.11.37

PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

Read data files from: /usr/share/nmap
Nmap done: 1 IP address (1 host up) scanned in 12.60 seconds
           Raw packets sent: 65535 (2.884MB) | Rcvd: 65535 (2.621MB)
````

Amb els ports resultants de l'escaneig anterior, enumerar la versió i llençar els scripts per defecte de NMAP.

````bash
> nmap -sCV -p22,80 -Pn 10.10.11.37

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 31:83:eb:9f:15:f8:40:a5:04:9c:cb:3f:f6:ec:49:76 (ECDSA)
|_  256 6f:66:03:47:0e:8a:e0:03:97:67:5b:41:cf:e2:c7:c7 (ED25519)
80/tcp open  http    Apache httpd 2.4.58
|_http-title: Did not follow redirect to http://instant.htb/
|_http-server-header: Apache/2.4.58 (Ubuntu)
Service Info: Host: instant.htb; OS: Linux; CPE: cpe:/o:linux:linux_kernel
````
Buscant la versió de SSH al launchpad d'Ubuntu ja es pot extreure que, segurament, el host té un Ubuntu Noble. D'altra banda, sabem que s'està aplicant _Virtual Hosting_ i, per tant, s'ha d'afegir el domini instant.htb a l'arxiu /etc/hosts per a que resolgui a la IP que pertoca.

## Web enumeration
La pàgina web mostra un botó de descàrrega que baixa un arxiu .apk, és a dir, una aplicació de mòbil. 

![image](https://github.com/user-attachments/assets/b3cc940f-5461-470f-ae07-935ce228ae17)

Les APK es poden descomprimir amb una eina que es diu _APKtool_, mostrant aleshores tot el codi i, possiblement, API Keys o contrasenyes hardcodejades. Un cop descomprimit podem cercar entre tots els fitxers que s'han generat per aquells que continguin alguna informació del domini "instant.htb".
````bash
> grep -r instant.htb
````
Un cop fet això trobem dos subdominis: _swagger-ui.instant.htb_ i _mywalletv1.instant.htb_. Els afegim al /etc/hosts. En concret, Swagger UI permet provar les funcionalitats d'una REST API sense accedir de forma directa al codi. L'altre subdomini, en canvi, redirigeix a un codi 404.

Tanamteix, si provem a executar algun endpoint, la resposta és un codi 401 avisant que necessitem autorització.

![image](https://github.com/user-attachments/assets/7aa4041d-f137-466c-a85a-07d45cdf166e)

 ## User
 En el panell d'autenticació se'ns diu que el token per autorizar-nos té el nom de "Authorization". Per tant, busquem entre el codi de l'APK si hi ha algun token amb aquest nom.
 
 ![image](https://github.com/user-attachments/assets/d4e93a71-f9a6-41a1-8a94-4f72805c2508)
````bash
> grep -r Authorization
````
I ens dóna diversos fitxers que contenen aquesta string, tot i que hi ha un que crida l'atenció: AdminActivities.smali, que té pinta que conté el codi de la part administrativa de l'aplicació. Efectivament, xafardejant l'arxiu hi trobem el JSON Web Token per poder executar endpoints de l'API.
````
Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicm9sZSI6IkFkbWluIiwid2FsSWQiOiJmMGVjYTZlNS03ODNhLTQ3MWQtOWQ4Zi0wMTYyY2JjOTAwZGIiLCJleHAiOjMzMjU5MzAzNjU2fQ.v0qyyAqDSgyoNFHU7MgRQcDA0Bw99_8AEXKGtWZ6rYA
````
Ara ja podem utilitzar totes les funcionalitats. De fet, en aquesta prova també hem pogut enumerar de passada el primer usuari del sistema: _shirohige_.

![image](https://github.com/user-attachments/assets/2afbe4a0-86ec-4148-aef7-eaf341d427cc)

Dues d'aquestes funcionalitats de l'API són llistar els logs disponibles i llegir-los, respectivament. Si mirem quins logs hi ha, trobem que hi ha un fitxer 1.log situat al path /home/shirohige/logs. Confirmem, doncs, que shirohige és un usuari del sistema, al qual hi tenim un potencial accés.

![image](https://github.com/user-attachments/assets/3046dd65-c3a2-4212-bee4-9dbec34fda64)

D'altra banda, si fem una petició per llegir aquest log, veiem que l'API demana per GET el fixter a l'URL _http://swagger-ui.instant.htb/api/v1/admin/read/log?log_file_name=1.log_. Si no està l'input ben sanititzat pot esdevenir-se una vulnerabilitat de Local File Inclusion. Provem, doncs, a demanar el fitxer /etc/passwd navegant uns quants directoris enrere.

![image](https://github.com/user-attachments/assets/81bc70f0-9621-42b1-a71f-acd0c51b90a0)

Tenim accés a llegir els fitxers del sistema. Com a més sabem que tenim accés al directori home de l'usuari _shirohige_ perquè és on estan situats els logs, podem provar a extreure la clau privada de SSH, si la té.

![image](https://github.com/user-attachments/assets/96515eb7-8a99-4adf-be59-b9ed1f717cca)

I sí que la té, així que podem copiar-la, arreglar el format i obtenir una consola per SSH com l'usuari en qüestió.

![image](https://github.com/user-attachments/assets/eb56c323-cd45-47ee-89eb-3ef2ad0d0ad3)

## Privilege escalation
En el directori /opt/backups/Solar-PuTTY hi ha un arxiu _sessions-backup.dat_. En primer lloc, Solar PuTTY és un client de Windows per connectar-se a sessions remotes a través de SSH. En segon lloc, aquest programa genera fitxers de sessió i els encripta. Tot i això, és possible desencriptar-los mitjançant un atac de força bruta, tal com fa aquest [script de Python](https://gist.github.com/xHacka/052e4b09d893398b04bf8aff5872d0d5).
````bash
# Portem el sessions-backup.dat a la nostra màquina
> scp shirohige@10.10.11.37:/opt/backups/Solar-PuTTY/sessions-backup.dat sesions-backup.dat
# Executem el script
python3 decrypt.py /usr/share/wordlists/rockyou.txt sessions-backup.dat
````
I se'ns genera un arxiu desencriptat amb data d'inici de sessió a Solar-Putty, entre la qual trobem un usuari _root_ i una contrasenya _12**24nzC!r0c%q12_. 

![image](https://github.com/user-attachments/assets/a41d24a8-89a7-49a2-ad39-65422a7d8bc9)

Si provem a establir una sessió com l'usuari root al host amb la contrasenya que acabem d'obtenir tindrem una consola amb privilegis.

![image](https://github.com/user-attachments/assets/6cefc555-59cc-4965-ba84-39f5ad3025c0)

Donant així per acabada aquesta màquina.
