import socket, sys, threading, json, asyncio

DEBUG = True

class TCPConnection:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True
    
    def getPort(self):
        return self.port

    def bind(self):
        address = (self.ip, self.port)
        self.sock.bind(address)

    def close(self):
        self.running = False
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((self.ip, self.port))
        self.sock.close()

    def send(self, ip, port, msg):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            address = (ip,port)
            s.connect(address)
            s.sendall(msg.encode('utf-8'))

    def listen(self, server, username):
        self.sock.listen(1)
        
        while self.running:
            if DEBUG:
                print("> Listening for connections...")
            connection, address = self.sock.accept()
            thread = threading.Thread(target=serve, args=(connection, address, server, username))
            thread.start()

def serve(connection, address, server, username):
    try:
        if DEBUG:
            print('> Connection from', address)
        while True:
            data = connection.recv(1024)
            if data:
                if DEBUG:
                    print('> Received: "%s"' % data.decode('utf-8'))
                parse(data.decode('utf-8'), server, username)
            else:
                break
    finally:
        connection.close()

# Message Format:
# set USERNAME CONTENT
# get USERNAME NUMBER_OF_MESSAGES

def parse(data, server, username):
    fragments = data.split(" ",2)
    print(fragments)

    if fragments[0] == "set":
        print("set...")
    elif fragments[0] == "get":
        print("get...")
