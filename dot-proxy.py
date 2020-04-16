#!/usr/bin/env python
from socketserver import BaseRequestHandler, ThreadingTCPServer, ThreadingUDPServer
import socket
import ssl
import sys
import multiprocessing


class DNSoverTCP(BaseRequestHandler):
    """ Handler for TCP requests"""
    def handle(self):
        try:
            # print('Got TCP connection from', self.client_address)
            while True:
                msg = self.request.recv(buffer_size)
                if not msg:
                    break
                answer = tls_wrapper(msg, hostname=nameserver)
                self.request.send(answer)
        except socket.timeout as err:
            print('TIMEOUT ERROR: ', err)
            return sys.exit(1)
        except socket.error as err:
            print('OTHER ERROR: ', err)
            self.request.close()
            return sys.exit(1)


class DNSoverUDP(BaseRequestHandler):
    """ Handler for UDP requests"""
    def handle(self):
        try:
            # print('Got UDP connection from', self.client_address)
            msg, sock = self.request
            tcp_packet = udp_to_tcp(msg)
            tls_answer = tls_wrapper(tcp_packet, hostname=nameserver)
            udp_answer = tls_answer[2:]
            sock.sendto(udp_answer, self.client_address)
        except socket.timeout as err:
            print('TIMEOUT ERROR: ', err)
            return sys.exit(1)
        except socket.error as err:
            print('OTHER ERROR: ', err)
            return sys.exit(1)


def tls_wrapper(packet, hostname, port=853):
    """SSL wrapper for socket"""
    context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
    with socket.create_connection((hostname, port), timeout=5) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as tlssock:
            tlssock.send(packet)
            result = tlssock.recv(buffer_size)
            return result


def udp_to_tcp(packet):
    """Converter for UDP packets"""
    packet_len = bytes([00]) + bytes([len(packet)])
    packet = packet_len + packet
    return packet


if __name__ == '__main__':
    nameserver = '1.1.1.1'
    proxy_addr = ''
    proxy_port = 5300
    buffer_size = 1024

    ThreadingTCPServer.allow_reuse_address = True
    ThreadingUDPServer.allow_reuse_address = True
    tcp_proxy = ThreadingTCPServer((proxy_addr, proxy_port), DNSoverTCP)
    udp_proxy = ThreadingUDPServer((proxy_addr, proxy_port), DNSoverUDP)

    tcp_process = multiprocessing.Process(target=tcp_proxy.serve_forever)
    udp_process = multiprocessing.Process(target=udp_proxy.serve_forever)

    tcp_process.start()
    print('DNS Proxy over TCP started and listening on port %s' % proxy_port)
    udp_process.start()
    print('DNS Proxy over UDP started and listening on port %s' % proxy_port)
