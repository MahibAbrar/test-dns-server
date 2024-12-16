from dnslib import DNSRecord
import socket
import socketserver

class DNSHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        try:
            request = DNSRecord.parse(data)
            print(f"Received request for: {str(request.q.qname)}\n")

            reply = DNSRecord()

            socket.sendto(reply.pack(), self.client_address)
        except Exception as e:
            print(f"Exception is: {e}")
if __name__ == "__main__":
    socketserver.UDPServer.allow_reuse_port = True
    server = socketserver.UDPServer(("0.0.0.0", 53), DNSHandler)
    print("Running at 53")
    server.serve_forever()