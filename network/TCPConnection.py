import socket, sys, threading, json, asyncio
from protocol import protocol_pb2 as Protocol
from termcolor import colored

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

    def connect(self):
        address = (self.ip, self.port)
        self.sock.connect(address)

    def send(self, ip, port, msg):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            address = (ip,port)
            s.connect(address)
            s.sendall(msg) 

    def send_and_receive(self, msg, timeline=None):
        try:
            self.sock.sendall(msg)
            data = self.sock.recv(1024)
            message = Protocol.OperationReply()
            message.ParseFromString(data)
            if data:
                process_message(message, None, timeline)
        finally:
            self.close()

    def listen(self, username, timeline):
        self.sock.listen(1)
        
        while self.running:
            if DEBUG:
                print("> Listening for connections...")
            connection, address = self.sock.accept()
            thread = threading.Thread(target=serve, args=(connection, address, username, timeline))
            thread.start()

    def isOnline(self, host, port):
        result = self.sock.connect_ex(host, port)
        return result == 0    

def serve(connection, address, username, timeline):
    try:
        if DEBUG:
            print('> Connection from', address)
        while True:
            data = connection.recv(1024)
            message = Protocol.Operation()
            message.ParseFromString(data)
            if data:
                process_message(message, connection, timeline)
            else:
                break
    finally:
        connection.close()

# Message Format:
# set USERNAME CONTENT (guarda localmente e caso exceda o limite, apaga as mais antigas) (prov. n vamos precisar disto, so do broadcast)
# get USERNAME NUMBER_OF_MESSAGES (devolve as n ultimas msgs)
# broadcast USERNAME CONTENT (envia a mais nodos, guarda localmente e caso exceda o limite, apaga as mais antigas)

def process_message(message, connection, timeline):
    
    if type(message) is Protocol.Operation:
        if message.type == Protocol.GET_TIMELINE:
            if DEBUG:
                print(colored('\n> Received GET TIMELINE request.\n', 'blue'))

                # create a reply msg and define the reply message type
                replyMessage = Protocol.OperationReply()
                replyMessage.type = Protocol.GET_TIMELINE;

                # create a timeline post message
                timeline_post = replyMessage.timeline.add()
                timeline_post.id = 1
                timeline_post.content = 'this is a test post'
                timeline_post.timestamp = 'test_timestamp'

                connection.sendall(replyMessage.SerializeToString())
        elif message.type == Protocol.PUBLISH:
            if DEBUG:
                print(colored('\n> Received BROADCAST request.\n', 'blue'))
    elif type(message) is Protocol.OperationReply:
        if DEBUG:
            print(colored('\n> Received GET TIMELINE reply message.\n', 'blue'))
            print(message)
    else: 
        if DEBUG:
            print(colored('\n> Received an unknown operation.\n', 'red'))