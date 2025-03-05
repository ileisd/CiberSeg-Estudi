# DNS Recon
El DNS, _Domain Name Server_, és un protocol que s'utilitza per resoldre direccions IP a noms de domini. És el responsable, doncs, de que es pugui accedir a una web a través del seu nom (github.com) i no haguem de memoritzar la seva adreça. Utilitza una estructura jeràrquica de servidors, que funciona, explicat de forma molt bàsica, de la següent manera:
1. L'usuari entra a una pàgina web a través del seu navegador.
2. Aquesta petició passa al DNS Resolver, normalment el del propi ISP però també pot ser extern, com el de Google (8.8.8.8) o Cloudflare (1.1.1.1).
3. El DNS Resolver envia la petició al Root DNS, i aquest la passa al Name Server del TLD corresponent.
4. El Name Server es comunica amb el DNS Resolver dient-li a quins servidors hi ha el domini que busca.
5. El DNS Resolver fa una petició a un dels servidors on hi ha el domini.
6. Aquest servidor retorna la IP de la pàgina que s'està buscant al DNS Resolver.
7. El DNS Resolver retorna el valor de la IP al navegador web.
8. Es fa la petició a la direcció IP.
##### Registres DNS
Els registres DNS són instruccions que es donen els servidors per la seva interacció. A nivell de reconeixement, ens poden donar informació sobre quina és la IP del domini, subdominis, servidors de correu... Els principals tipus són:

|           |                                             |
| --------- | ------------------------------------------- |
| **A**     | resol un domini a una direcció IPv4         |
| **AAAA**  | resol un domini a una direcció IPv6         |
| **CNAME** | dirigeix un alias al nom canònic            |
| **NS**    | nom del servidor DNS autoritzat             |
| **MX**    | dirigeix els correus al servidor del domini |
| **TXT**   | nota de text (prevenció de spam)            |
| **HINFO** | sistema operatiu i cpu del host             |
| **SOA**   | informació del domini o zona                |
| **SRV**   | servidor i port per serveis específics      |
| **PTR**   | IP a nom de domini                          |
```bash
dnsrecon -d [domini] # Mostra els registres DNS del domini
```
Hi ha la possibilitat de que hi hagi un firewall que no permeti la connexió directa al servidor, com CloudFlare, i que per tant no es pugui saber la IP real. En aquest cas, és interessant mirar els registres del servidor de mail, ja que CloudFlare no amagar la IP en aquest cas. Per saber si hi ha un firewall, es pot utilitzar:
```bash
host [domini]
```

## DNS Zone Transfer
Una de les millors tècniques per enumerar DNS és fer una transferència de zona, que hauria d'estar desactivada per seguretat. Consisteix en copiar tota la base de dades DNS d'un servidor primari a un altre controlat per nosaltres. En aquest cas podríem veure al 100% la forma de la xarxa objectiu, inclús les adreces privades.
```bash
dig axfr [@NameServer] [domini]
```

## DNSSEC
Pel funcionament del protocol DNS, seria molt fàcil fer-se passar per un servidor DNS i falsificar la IP que hi ha associada a un domini. Per aquest motiu s'utilitza DNSSEC, un protocol de seguretat basat en criptografia asimètrica que verifica la integritat de les peticions i les respostes de DNS.

En cas que no estigui configurat, el host és susceptible a atacs de phising o altres atacs de falsificació.