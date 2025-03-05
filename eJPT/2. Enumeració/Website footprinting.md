# Website footprinting
Internet és el nostre millor amic pel que fa a l'enumeració web. L'objectiu és trobar totes les tecnologies que s'utilitzen en el servei web, així com informació que pugui ser útil de cara al futur atac com correus electrònics, usuaris, noms de treballadors, altres dominis...   
Hi ha eines que automatitzen la detecció de tecnologies, com **Wappalyzer** (extensió de navegador) o **WhatWeb** (eina de terminal), entre moltíssimes altres. Tanmateix, sempre és millor fer una repassada manual amb diferents tècniques:
- Buscar icones de XXSS per extreure informació de les Xarxes Socials.
- Mirar l'arxiu /robots.txt per trobar directoris no indexats.
- Mirar l'arxiu /sitemap.xml per veure l'estructura de la web.
```bash
whatweb [url] # Enumeració de tecnologies i versions
```
## Whois enumeration
El _whois_ és un registre que mostra tota la informació relacionada amb un domini. En cas que no hi hagi cap censura configurada, que sol ser lo més normal en la majoria de casos, pot donar informació valuosa com direccions, telèfons, correus, noms o caducitat del domini. Es pot consultar a la web [Whois](https://who.is/) o la terminal amb:
```bash
whois [domini]
```
## WAF detection
Un WAF (Web Application Firewall) és una defensa del protocol de capa 7 que filtra i monitoreja el tràfic HTTP d’un servei web. Serveix per protegir d’atacs com el CSRF, SQLi o XSS. Una forma de WAF és un proxy invers, el que significa que protegeix de que agents exteriors puguin accedir directament al servidor i conéixer la IP real. Per exemple, CloudFlare és un WAF.
```bash
wafw00f [url] -a # Proves de detecció de WAF
```

## Subdomain enumeration
Tenir localitzats els subdominis d'un domini serveix per ampliar la mira de l'atac. És possible que el domini principal no tingui cap funcionalitat vulnerable o cap informació interessant però que hi hagi un subdomini que contingui informació sensible o permeti execució de comandes remotament per una vulnerabilitat.
```bash
sublist3r -d [domini] # Enumeració passiva a través de motors de cerca

wfuzz -c -w [wordlist] -r [url] -H "Host: FUZZ.[domini]" # Força bruta

amass enum --passive -d [domini] # Diverses tècniques
```

## Google Dorks
Les cerques a Google permeten l'ús de filtres que ens permeten acotar-la a les nostres necessitats, ja sigui per un tipus d'arxiu en concret, un domini... Hi ha una base de dades de [Google Dorks]([https://www.exploit-db.com/google-hacking-database](https://www.exploit-db.com/google-hacking-database)) on es poden consultar moltíssims filtres, tot i que els principals que s'utilitzen són:

		1. site:
		2. inurl:
		3. intitle:
		4. filetype:
		5. cache:

## Email & password leaks
S'han donat molts casos de fallides de seguretat en organitzacions que han causat una filtració de dades, les quals es solen publicar o vendre a la Deep Web. En un cas d'auditoria, es pot donar el cas que un dels objectius ha estat víctima i és possible que es puguin utilitzar les credencials o els correus filtrats en el nostre favor. Per comprovar-ho, hi ha la web [Have I Been Pwned?](https://haveibeenpwned.com/). En el cas del emails, també és possible que siguin públics, pel que es pot automatitzar una cerca als principals motors amb:
```bash
theHarvester -d [domini] -b [motors]
```