<p align="center">
  <img src="https://github.com/user-attachments/assets/49f49f6b-b80d-405d-968c-4c5f4f8704ac" alt="unrested-htb-header" width="50%" height="50%">
</p>

---

## NMAP scanning
Escaneig a través d'enviament de paquets TCP SYN a tots els ports del host per detectar quins estan oberts.
````bash
❯ nmap -p- --open -sS -v -n --min-rate=5000 -Pn -n 10.10.11.50

PORT      STATE SERVICE
22/tcp    open  ssh
80/tcp    open  http
10050/tcp open  zabbix-agent
10051/tcp open  zabbix-trapper

Read data files from: /usr/share/nmap
Nmap done: 1 IP address (1 host up) scanned in 12.34 seconds
           Raw packets sent: 65535 (2.884MB) | Rcvd: 65535 (2.621MB)                                                             
````
Amb els ports resultants de l'escaneig anterior, enumerar la versió i llençar els scripts per defecte de NMAP.
````bash
❯ nmap -sCV -p22,80,10050,10051 -Pn 10.10.11.50

PORT      STATE SERVICE             VERSION
22/tcp    open  ssh                 OpenSSH 8.9p1 Ubuntu 3ubuntu0.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 3e:ea:45:4b:c5:d1:6d:6f:e2:d4:d1:3b:0a:3d:a9:4f (ECDSA)
|_  256 64:cc:75:de:4a:e6:a5:b4:73:eb:3f:1b:cf:b4:e3:94 (ED25519)
80/tcp    open  http                Apache httpd 2.4.52 ((Ubuntu))
|_http-server-header: Apache/2.4.52 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
10050/tcp open  tcpwrapped
10051/tcp open  ssl/zabbix-trapper?
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Wed Mar 12 00:22:33 2025 -- 1 IP address (1 host up) scanned in 15.44 seconds        
````
Buscant la versió de SSH al launchpad d'Ubuntu ja es pot extreure que, segurament, el host té un Ubuntu Focal.

## Web enumeration
La màquina comença amb unes credencials que ens han donat: _matthew:96qzn0h2e1k3_. Amb aquestes, podem iniciar sessió al que sembla un servei de Zabbix, un sistema de monitorització de xarxes. A la pàgina que se'ns redirigeix, si mirem la part inferior, descobrim que, en concret, és Zabbix 7.0.0.

![image](https://github.com/user-attachments/assets/96755d87-eb60-4499-aa38-aa8389915fef)

Buscant per Internet, es pot trobar que aquesta versió té diverses vulnerabilitats, entre les que es troba una vulnerabilitat crítica de SQLi associada al mètode _user.get_ de la seva API. Si tenim accés a l'API podem explotar-la per obtenir el token d'autenticació de l'administrador i, posteriorment, crear un ítem per obtenir una reverse shell al servidor.
````sql
$db_roles = DBselect(
				'SELECT u.userid'.($options['selectRole'] ? ',r.'.implode(',r.', $options['selectRole']) : '').
				' FROM users u,role r'.
				' WHERE u.roleid=r.roleid'.
				' AND '.dbConditionInt('u.userid', $userIds)
			);
````
Aquesta és la peça de codi vulnerable. El valor de _$options['selectRole']_ passa un input controlat per l'usuari directament a la query SQL, sense aplicar capi tipus de sanitització ni filtre.

## User
Podem automatitzar aquesta explotació amb un script de [godylockz](https://github.com/godylockz/CVE-2024-42327/tree/main), que obté el token de l'administrador mitjançant time-based queries per després executar el mètode _item.create_ de l'API amb el codi de la reverse shell.

![image](https://github.com/user-attachments/assets/c425d97c-1351-4252-8428-c4e656d5fa83)

I obtenim satisfactòriament una pseudoconsola com l'usuari _zabbix_.

## Privilege escalation
Aquest usuari té permisos per executar sense contrasenya el binari situat a _/usr/bin/nmap_ amb tots els arguments que vulguem. Per tant, amb el codi que proporciona GTFOBins podem provar d'escalar privilegis utilitzant NNAP amb Sudo.

![image](https://github.com/user-attachments/assets/67f62406-e918-490e-a75f-006dd77163bd)

Tanmateix, quan provem a executar nmap de forma interactiva per obtenir una consola com a root, salta un avís que diu que "el mode interactiu està desactivat per raons de seguretat". Fa pensar, doncs, que s'estan aplicant restriccions al binari. Per tant, mirem el codi.

![image](https://github.com/user-attachments/assets/d5c146ed-a9bc-47e0-b505-6c67ee375eae)

Abans d'executar el binari original, aquest Nmap "personalitzat" fa una mena de firewall per a que no poguem utilitzar cap dels arguments que ens permeten escalar privilegis.

![image](https://github.com/user-attachments/assets/81ad2276-119f-4324-9331-9442fc94d865)

Així doncs, hem de trobar alguna altra flag que ens permeti executar codi de forma arbitrària, ja que no podem utilitzar scripts, fitxers ni el format interactiu. Mirant el manual, hi ha la possibilitat d'especificar quin és el directori que volem utilitzar per carregar els fitxers de dades de NMAP.
````bash
--datadir <dirname>: Specify custom Nmap data file location
````
A la documentació es descriu que els fitxers de dades de Nmap són 7 fitxers, que comencen amb el prefix "nmap-", que s'encarreguen de l'escaneig de ports i altres operacions. Es troben, normalment, a _/usr/share/nmap_ N'és un exemple _nmap-services_, que relaciona el número de port amb el servei que sol associar-se comunment. 

Són scripts escrits en Lua, per tant, com podem especificar el directori on volem que Nmap busqui aquests fitxers, podem crear un fitxer en un directori arbitrari amb codi en Lua per a que ens crei una consola (que s'executarà amb privilegis de root perquè executarem el Nmap amb sudo). Tot i que es pot fer amb qualsevol dels arxius, jo decideixo fer-ho amb _nse_main.lua_, que agafa tots els scripts que tenen la categoria "default" i, per tant, s'executa quan s'especifica la flag _-sC_.
````bash
# Creem el fitxer 
> echo 'os.execute("/bin/bash")' > /tmp/nse_main.lua
````
I quan executem Nmap, automàticament ens dóna una consola amb privilegis de root.

![image](https://github.com/user-attachments/assets/259c35ed-4b32-48b9-9480-f835b654c7ec)

