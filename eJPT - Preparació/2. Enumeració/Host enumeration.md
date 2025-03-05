## Service version detection
Quan es descobreix un port obert, Nmap utilitza la seva base de dades de serveis comuns per determinar automàticament què s'està utilitzant en aquell port. Tot i que no és una detecció "real", sí que correspon la majoria de cops a la veritat, ja que tots els serveis tenen uns ports estàndard assignats i, per tant, la gran majoria de cops seran els mateixos. Els principals ports TCP són:
- **FTP:** 21
- **SSH:** 22
- **SMTP**: 25
- **DNS**: 53
- **HTTP**: 80/8080
- **NetBios**: 139
- **HTTPS:** 443
- **SMB**: 445
- **MySQL:** 3306
- **RDP**: 3389
- **WinRM**: 47001
Tot i això, no és útil només saber el servei, ja que no aporta molta informació de cara a l'explotació. Per aquest motiu, es fa una connexió al port especificat per rebre la capçalera del servei que hi ha actiu, on normalment es mostra el servei específic emprat i la versió.
```bash
telnet [ip] [port]
nmap -sV [port] [ip]
```

## OS detection
Si hi ha un port obert i un port tancat, Nmap pot determinar, a través de certes proves amb la comunicació TCP, quin és el sistema operatiu del host objectiu. És una detecció estadística en la que relaciona els resultats de les proves amb la seva base de dades, per lo qual no es pot tractar com una detecció 100% eficaç i s'ha de complementar amb altres mecanismes (TTL, launchpad...).
```bash
nmap -O [IP] # Detecció del sistema operatiu
	--oscan-guess #Forçar les probabilitats
	--version-intensity #Agressivitat de les proves
```

## Nmap scripts
Al directori _/usr/share/nmap/scripts_ hi ha una sèrie d'arxius de codi, escrits majoritàriament en Lua, amb extensió .nse que realitzen proves d'enumeració per a serveis detectats. Estan organitzats en diferents categories, segons servei i funcionalitat entre d'altres, i una d'aquestes categories és "per defecte": una agrupació dels scripts bàsics de reconeixement que es poden llençar junts.
```bash
nmap -sC [ip] #Utilitza tots els scripts "per defecte" 
```
Tanmateix, hi ha vegades que es necessita un script  o categoria específics per dur a terme una tasca concreta. En aquests casos, es pot localitzar el script de les següents formes:
```bash
find /usr/share/nmap/scripts/ -name [servei]* # Tots els scripts d'un servei

grep [categoria] /usr/share/nmap/scripts/* # Tots els serveis de la categoria
```
Un cop localitzat, es pot veure el funcionament i la sintaxi del script:
```bash
nmap --script-help=[script]
```
I per utilitzar-lo, només s'ha d'incloure a la comanda:
```bash
nmap --script=[script]
	--script-args=[args] # Amb els arguments necessaris, si s'escau
```