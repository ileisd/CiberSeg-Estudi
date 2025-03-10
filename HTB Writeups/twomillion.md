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

## Foothold
