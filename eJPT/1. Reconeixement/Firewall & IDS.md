# Firewall & IDS
Nmap ofereix la possibilitat de modificar els paquets enviats, tant a nivell d'informació com de freqüència, per tal de poder burlar la detecció d'intrusions i el filtratge de paquets.
```bash
nmap -sA -p [port(s)] [ip] # Detectar si hi ha firewall filtrant el port
```
Si hi ha un firewall bloquejant certs tipus de paquets, s'ha de provar amb els diferents tipus d'escaneig de [[Host Discovery#TCP Ping|TCP]].
## IDS evasion
##### Size and data fragmentation
Com les connexions TCP permeten l'ordenació de paquets a l'arribada, és possible fragmentar aquests, de manera que el seu tamany és menor i la informació dispersa dificulta l'anàlisi però tenim la certesa que arribaran de forma fiable i en l'ordre correcte.
```bash
nmap -f --mtu [bytes] # Fragmentació dels paquets en màxim [] bytes. 
```
També és possible determinar el tamany màxim dels paquets enviats sense fragmentació, molt útil quan hi ha un firewall que bloqueja paquets de 0 bytes:
```bash
nmap --data-length [tamany]
```
O canviar la IP i el port d'origen dels paquets (tot i que en els SYN-ACK i RST de resposta s'inclou la IP original):
```bash
nmap -D [ip(s)] -g [port] 
```
##### Scan optimization
És la modulació de la freqüència d'enviament dels paquets. A banda de l'IDS, aquest apartat és útil per evitar una denegació de servei a la xarxa.
```bash
nmap --host-timeout [n] # Desistir al cap de n temps sense resposta
nmap --scan-delay [n] # Esperar n segons entre proves a hosts
nmap --min-rate [n] || nmap --max-rate [n] # mínim/màxim de n paquets per segon
nmap -T [0-5] # Plantilles predeterminades (0=paranòic, 5=el diaablo)
```