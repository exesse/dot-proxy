# dot-proxy
Python implementation for DNS over TLS proxy server.

Listens for both TCP and UDP packet on native 53 port. Converts plain UDP packets to TCP by prefixing message with a 
two bytes length field which the incoming UDP message have [[1]](#1).

By default establishes SSL connection with CloudFlare DNS (1.1.1.1) over 853 port. Python function 
'create_default_context' from build-in ssl library used to establish connection with nameserver. 
The function loads system's trusted CA certificates, does hostname checking and sets reasonable secure 
protocol and cipher settings [[2]](#2).

Default buffer size is set to 1024, which should be sufficient for most DNS queries.
Socket has 5 seconds timeout which corresponds with default timeout of dns tools like 'dig' or 'kdig'. 

###### HOW TO RUN

**Option 1.**

Pull docker container from dockerhub.

`docker run {-d -p <localport>:53 -p <localport>:53/udp --name <container_name>} exesse/dot-proxy`

**Option 2.**

Run source code directly.

`sudo ./dot-proxy.py`

*by default non-root users are not allowed to use ports below 1024 on *nix systems. Please also make sure that port 53 
is not in use and firewall software allows incoming connections to the mentioned port. To start proxy on custom local 
port by adjusting 'proxy_port' variable in 'dot-proxy.py' file.   

###### HOW TO TEST

Test example with 'kdig' tool:

````bash
# TCP Version
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

# UDP Version 
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

###### QUESTIONS

**Security concerns**

* Prone to denial of service attacks. Could be resolved by specifying maximum pool size of threads for TCP/UDP servers.
* Still prone to spoofing in between client and proxy communications.
* Trusted CA should be explicitly specified.
* BIND 9 does not support TLS by default. This means if the first nameserver does not have record we are querying for 
it may simply fallback to plian tcp in recursion to another nameserver [[3]](#3). 
* Could be combined with DNS over HTTPS(DoH) to compromise local network policies or restrictions.


**Microservices integration**
* Comes packed as docker container and ready to be deployed
* Could be combined with load balancer in docker-compose file to perform some sort of round-robin.* 
* For deployment in k8s the proxy should be explicitly specified as nameserver or kube-dns(CoreDNS) should be configured 
respectively.   


**Improvements**
* To speedup queries caching should be used.
* Temporary block for the client that sends too much queries at a time should be implemented.
* Correct thread termination on system signals should be implemented.
* Error handlers should be added. 
* Fallback on other public\private DNS over TLS(DoT) server should be implemented.
* Extra layer of security which compares query's result with other DoT may be added.**
* Lame Duck State could be added to inform about overload and explicitly requests client to send request to other server.
* Monitoring and\or alerting features could be added.

**Notes**

\*Popular load balancer NGINX also could be configured to proxy DNS over TLS queries [[4]](#4).

** Will decently have negative impact on performance. And some sort of quorum needed to identify which of the record is 
correct in case of mismatch.  

**Links**

<a id="1">[1]</a> 
RFC1035 - Domain names - implementation and specification.
Link: 
https://tools.ietf.org/html/rfc1035

<a id="1">[2]</a>
ssl — TLS/SSL wrapper for socket objects. 
Link: 
https://docs.python.org/3/library/ssl.html

<a id="1">[3]</a>
DNS over TLS - BIND 9.
Link: 
https://kb.isc.org/docs/aa-01386

<a id="1">[4]</a>
Using NGINX as a DoT or DoH Gateway.
Link:
https://www.nginx.com/blog/using-nginx-as-dot-doh-gateway
