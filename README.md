# dot-proxy
Python implementation of simple DNS over TLS proxy server.

Listens for both TCP and UDP messages on native 53 port. Converts plain UDP packets to TCP by prefixing message with a 
two bytes length field which the incoming UDP message have [[1]](#1).

By default establishes SSL connection with Cloudflare DNS (1.1.1.1) over 853 port. Python function 
'create_default_context' from build-in **ssl** library was used to establish connection with nameserver. 
The function loads system's trusted CA certificates, does hostname checking and sets reasonable secure 
protocol and cipher settings [[2]](#2).

Default buffer size is set to 1024, which is sufficient for most DNS queries. Socket is set to 5 seconds timeout which 
corresponds with the default timeout of dns tools like 'dig' or 'kdig'. 

#### HOW TO RUN
* Option 1:

Pull docker container from github:

`docker pull docker.pkg.github.com/exesse/dot-proxy/dot_proxy:1.0.0`

Start pulled container:

`docker run -d --name dot_proxy docker.pkg.github.com/exesse/dot-proxy/dot_proxy:1.0.0`

* Option 2:

Make source code executable:

'chmod +x dot_proxy.py'

Set 'PROXY_PORT' variable to some unused port like `5300`

Start executable app by running the following:  

`./dot-proxy.py`

*by default non-root users are not allowed to use ports below 1024 on *nix systems. Please make sure that port 53 
is not in use and firewall software allows incoming connections to the mentioned port. To start proxy on custom 
port simply adjust 'proxy_port' variable in 'dot-proxy.py' file.   

#### HOW TO TEST

'Dig', 'kdig', 'drill', 'wireshark' could be used for testing. Here is a TCP test example performed with 'kdig' tool.

````bash
kdig @172.17.0.2 google.com A +tcp

;; ->>HEADER<<- opcode: QUERY; status: NOERROR; id: 8769
;; Flags: qr rd ra; QUERY: 1; ANSWER: 1; AUTHORITY: 0; ADDITIONAL: 0

;; QUESTION SECTION:
;; google.com.                  IN      A

;; ANSWER SECTION:
google.com.             75      IN      A       172.217.19.78

;; Received 54 B
;; Time 2020-09-05 19:42:43 CEST
;; From 172.17.0.2@53(TCP) in 127.2 ms
````

And here is another example again with 'kdig', but this time over UDP.  
```bash
kdig @172.17.0.2 google.com AAAA

;; ->>HEADER<<- opcode: QUERY; status: NOERROR; id: 51129
;; Flags: qr rd ra; QUERY: 1; ANSWER: 1; AUTHORITY: 0; ADDITIONAL: 0

;; QUESTION SECTION:
;; google.com.                  IN      AAAA

;; ANSWER SECTION:
google.com.             187     IN      AAAA    2a00:1450:4005:80b::200e

;; Received 66 B
;; Time 2020-09-05 19:43:05 CEST
;; From 172.17.0.2@53(UDP) in 141.0 ms
````

**Links**

<a id="1">[1]</a> 
RFC1035 - Domain names - implementation and specification.
Link: 
https://tools.ietf.org/html/rfc1035

<a id="1">[2]</a>
ssl — TLS/SSL wrapper for socket objects. 
Link: 
https://docs.python.org/3/library/ssl.html
