from dnslib import DNSRecord
import socket
import socketserver
from flask import Flask, request, render_template_string, jsonify
import threading

print("INIT THIS APP ")

app = Flask(__name__)
@app.route('/')
def index():
    return jsonify(status=200)

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
            print(f"Exception: {e}")
def start_socketserver():
    print("Attempt to run ...")
    socketserver.ThreadingUDPServer.allow_reuse_port = True
    server = socketserver.ThreadingUDPServer(("0.0.0.0", 53), DNSHandler)
    print("Running at 53")
    server.serve_forever()
    print("Complete")
def start_flask():
    app.run(host="0.0.0.0", port=80)

t1 = threading.Thread(target=start_socketserver)
t2 = threading.Thread(target=start_flask)


t1.start()
t2.start()
