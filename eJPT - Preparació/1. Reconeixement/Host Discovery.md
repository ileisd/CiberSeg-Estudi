En una xarxa local, cada host té assignada una IP única dins el rang establert, que permet la comunicació entre els diferents sistemes connectats. Aquest rang està reglat pel _CIDR (Classless Inter-Domain Routing)_ o la _netmask_, que indiquen la quantitat màxima d'adreces que pot haver a la xarxa i, per tant, la quantitat màxima de hosts que hi pot haver connectats.

Les principals subxarxes que hi ha són:

| CIDR | Netmask       | Total d' IP | IP útils |
|----- |---------------|-------------|----------|
| /8   | 255.0.0.0     | 16777216    | 16777214 |
| /12  | 255.240.0.0   | 1048576     | 1049574  |
| /16  | 255.255.0.0   | 65536       | 65534    |
| /20  | 255.250.240.0 | 4096        | 4094     |
| /24  | 255.255.255.0 | 256         | 254      |
> Les adreces útils són 2 menys que el total perquè les x.x.x.0 i x.x.x.255 estan reservades a identificar la pròpia subxarxa i a la comunicació amb la resta de hosts, respectivament.
## Ping sweep
És l'enviament de traces ICMP a totes les adreces possibles de la xarxa. Si un host contesta amb un _Echo Reply_ al nostre _Echo Request_, significa que està actiu. Si no contesta, segurament estigui inactiu, tot i que pot ser que sigui un fals negatiu per un firewall bloquejant la comunicació (com és el cas de Windows) o per congestió de la xarxa.
```bash
fping -a -g [Rang IP]

nmap -sn -PE [Rang IP] # En xarxes internes, afegir --send-ip

for i in {1..254} ;do (ping -c 1 [ip] &) ;done # Linux per subnets /24

for /L %i in (1,1,255) do @ping -n 1 -w 200 192.168.1.%i > nul && echo 192.168.1.%i is up. # windows per subnets /24
```
## ARP Scanning
L'_Address Resolution Protocol_ és l'enllaç entre la capa 2 i la capa 3 del Model OSI. S'encarrega de resoldre les adreces MAC dels hosts de la xarxa a partir de la seva IP per a que puguin comunicar-se entre ells. A més, com és un protocol essencial, no es pot bloquejar, pel que és molt fiable per aplicar Host Discovery, encara que requereix de privilegis d'administrador.
```bash
sudo nmap -sn [Rang IP]
sudo arp-scan --localnet
sudo netdiscover -i [interface]
```
## TCP Ping
TCP és un protocol de connexió que es caracteritza per rebre la informació de forma fiable i ordenada. Estableix una connexió entre l'emisor i el destinatari abans de començar l'intercanvi de dades, a través del _Three-way Handshake_:

**1. SYN:** el client envia un paquet amb la intenció d'establir una connexió. En aquest paquet, inclou un número de seqüència (ISN).
**2. SYN-ACK:** el servidor rep el paquet amb els bits SYN i envia un ACK amb el ISN+1 de l'emisor, més el seu propi ISN.
**3. ACK:** l'emisor rep els bits SYN del servidor i estableixen la connexió sobre la qual comença la transferència de dades, on cada paquet porta els bits ACK i ISN+1.

Per descobrir hosts d'una xarxa, es pot jugar amb aquests tipus de paquets TCP, segons les necessitats. Val a dir que aquest tipus de escaneig ha d'anar dirigit a un port en concret, per com funciona el protocol:
##### TCP SYN Ping
No estableix connexió, envia un TCP SYN i després un TCP RST. Si el destinatari està actiu, retornarà el SYN amb un SYN-ACK. És molt sigilós i més ràpid que una connexió normal.
```bash
nmap -sn -PS [port] [Rang IP]
```
##### TCP ACK Ping
Envia directament un paquet TCP ACK, en espera d'un TCP RST si el host està actiu. Normalment, aquest tipus de connexions estan bloquejades pel firewall, així que no és recomanable.
```bash
nmap -sn -PA [port] [Rang IP]
```

## UDP Ping
UDP és un protocol sense connexió que, si bé és més ràpid de TCP, no assegura la fiabilitat ni ordre de la informació. Cada paquet es transmet de forma independent entre emissor i receptor, sense cap tipus de persistència ni mecanisme d'integritat. S'utilitza molt per serveix que requereixin baixa latència, com streams i VoIP. 

Només s'hauria d'utilitzar el UDP Ping quan no hi ha cap port exposat per TCP i l'ICMP està bloquejat.
```bash
nmap -sn -PU [port] [Rang IP]
```

## Port scanning
En una xarxa hi ha **65535** ports. Per tant, com els escanejos per TCP i UDP han d'estar dirigits a un port en concret, és interessant poder decidir quins són els ports objectiu que ens interessen. També és interessant fer un escaneig de tots els ports, o dels ports més comuns, per determinar quins d'aquests estan oberts i, en última instància, quin servei i versió córren.
```bash
nmap -p [port]
nmap -p [port,port,port...] # Llista de ports
nmap -p- # Tots els ports
nmap -p [port-port] # Rang de ports
nmap -F # 100 ports més comuns
nmap --top-ports[n] # n ports més comuns
```
