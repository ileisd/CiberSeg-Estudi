<p align="center">
  <img src="https://github.com/user-attachments/assets/67d6ce83-549a-4d19-bf3f-9e20ff2fb6bb" alt="twomillion-htb-header" width="700" height="500">
</p>

---
## NMAP Scanning
Escaneig a través d'enviament de paquets TCP SYN a tots els ports del host per detectar quins estan oberts.
````bash
> nmap -p- --open -sS -v -n --min-rate=5000 -Pn -n 10.10.11.221

Host is up (0.072s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

Read data files from: /usr/share/nmap
Nmap done: 1 IP address (1 host up) scanned in 12.52 seconds
           Raw packets sent: 65562 (2.885MB) | Rcvd: 65562 (2.622MB)
````
Amb els ports resultants de l'escaneig anterior, enumerar la versió i llençar els scripts per defecte de NMAP.
````bash
> nmap -sCV -p22,80 -Pn 10.10.11.221

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 3e:ea:45:4b:c5:d1:6d:6f:e2:d4:d1:3b:0a:3d:a9:4f (ECDSA)
|_  256 64:cc:75:de:4a:e6:a5:b4:73:eb:3f:1b:cf:b4:e3:94 (ED25519)
80/tcp open  http    nginx
|_http-title: Did not follow redirect to http://2million.htb/
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 9.88 seconds
````
Buscant la versió de SSH al launchpad d'Ubuntu ja es pot extreure que, segurament, el host té un Ubuntu Jammy. D'altra banda, sabem que s'està aplicant _Virtual Hosting_ i, per tant, s'ha d'afegir el domini 2million.htb a l'arxiu /etc/hosts per a que resolgui a la IP que pertoca.
