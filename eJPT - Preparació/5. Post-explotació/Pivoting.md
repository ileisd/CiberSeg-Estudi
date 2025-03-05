La xarxa d'una organització pot estar segmentada en diferents parts per conveniència o seguretat, de manera que uns hosts no poden connectar-se amb uns altres. Es pot donar el cas, també, que un d'aquests hosts estigui dins els dos segments i tingui accés a les dues xarxes.

Si s'aconsegueix comprometre aquest host, es pot tenir accés a la xarxa no visible inicialment a través del _pivoting_, una redirecció del tràfic des del sistema atacant fins la víctima del nou segment, utilitzant la màquina ja compromesa com a intermediària. Hi ha diverses maneres d'aconseguir aquesta redirecció, tot i que l'esquema general és:
1. Redireccionar un port de la màquina víctima a un port de la màquina local.
2. Establir un socks proxy per passar tot el tràfic entre els ports dels dos hosts.
## SSH + ProxyChains
```bash
ssh -D [port] [user]@[host] # Dynamic port forwarding
echo "socks5 [ip_intermediaria] [port]" > /etc/proxychains4.conf # socks proxy
proxychains4 [command]
```
## Metasploit + ProxyChains
```bash
# mòduls de msfconsole:
route
socks_proxy

# bash
echo "socks5 [ip_intermediaria] [port]" > /etc/proxychains4.conf # socks proxy
proxychains4 [command]
```

> Per fer un escaneig amb Nmap a la nova xarxa, s'ha de fer un TCP Scan amb la opció -sT per a que funcioni.