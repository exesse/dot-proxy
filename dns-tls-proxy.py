from socketserver import BaseRequestHandler, TCPServer, UDPServer
import socket
import ssl


class DNSoverTCP(BaseRequestHandler):
    def handle(self):
        print('Got TCP connection from', self.client_address)
        while True:
            msg = self.request.recv(socket_size)
            if not msg:
                break
            answer = tls_wrapper(msg, hostname=nameserver)
            self.request.send(answer)


class DNSoverUDP(BaseRequestHandler):
    def handle(self):
        print('Got UDP connection from', self.client_address)
        msg, sock = self.request
        tcp_packet = udp_to_tcp(msg)
        tls_answer = tls_wrapper(tcp_packet, hostname=nameserver)
        udp_answer = tls_answer[2:]
        sock.sendto(udp_answer, self.client_address)


def tls_wrapper(packet, hostname, port=853):
    context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
    with socket.create_connection((hostname, port), timeout=5) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            ssock.send(packet)
            result = ssock.recv(socket_size)
            return result


def udp_to_tcp(packet):
    packet_len = bytes([00]) + bytes([len(packet)])
    packet = packet_len + packet
    return packet


if __name__ == '__main__':
    nameserver = '8.8.8.8'
    socket_size = 1024
    proxy_port = 5005
    serv = UDPServer(('', proxy_port), DNSoverUDP)
    serv.serve_forever()
