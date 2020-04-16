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

**Option 1.**

Pull docker container from dockerhub.

`docker run {-d -p <localport>:53 -p <localport>:53/udp --name <container_name>} exesse/dot-proxy`

**Option 2.**

Run source code directly.

`sudo ./dot-proxy.py`

*by default non-root users are not allowed to use ports below 1024 on *nix systems. Please make sure that port 53 
is not in use and firewall software allows incoming connections to the mentioned port. To start proxy on custom 
port simply adjust 'proxy_port' variable in 'dot-proxy.py' file.   

#### HOW TO TEST

'Dig', 'kdig', 'drill', 'wireshark' could be used for testing. Here is a TCP test example performed with 'kdig' tool.

````bash
kdig @172.17.0.2 n26.com A +tcp
;; ->>HEADER<<- opcode: QUERY; status: NOERROR; id: 6574
;; Flags: qr rd ra; QUERY: 1; ANSWER: 1; AUTHORITY: 0; ADDITIONAL: 0

;; QUESTION SECTION:
;; n26.com.            		IN	A

;; ANSWER SECTION:
n26.com.            	44	IN	A	128.65.211.162

;; Received 48 B
;; Time 2020-04-02 16:40:02 CEST
;; From 172.17.0.2@53(TCP) in 152.7 ms
````

And here is another example again with 'kdig', but this time over UDP.  
```bash
kdig @172.17.0.2 n26.com AAAA
;; ->>HEADER<<- opcode: QUERY; status: NOERROR; id: 58993
;; Flags: qr rd ra; QUERY: 1; ANSWER: 0; AUTHORITY: 1; ADDITIONAL: 0

;; QUESTION SECTION:
;; n26.com.            		IN	AAAA

;; AUTHORITY SECTION:
n26.com.            	155	IN	SOA	ns-1688.awsdns-19.co.uk. awsdns-hostmaster.amazon.com. 1 7200 900 1209600 86400

;; Received 116 B
;; Time 2020-04-02 16:34:59 CEST
;; From 172.17.0.2@53(UDP) in 175.4 ms
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
