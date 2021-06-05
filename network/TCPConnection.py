import socket, threading
from protocol import protocol_pb2 as Protocol
from termcolor import colored

from storage import followings_manager

DEBUG = True
MAX_NR_MESSAGES = 10


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

    def send_and_receive(self, msg, following):
        try:
            self.sock.sendall(msg)
            data = self.sock.recv(1024)
            message = Protocol.OperationReply()
            message.ParseFromString(data)
            if data:
                process_message(message, None, None, None, following)
        finally:
            self.close()

    def listen(self, username, timeline, following):
        self.sock.listen(1)

        while self.running:
            try:
                if DEBUG:
                    print("> Listening for connections...")
                connection, address = self.sock.accept()
                thread = threading.Thread(target=serve,
                                          args=(connection, address, username, timeline, following))
                thread.start()
            except KeyboardInterrupt:
                self.sock.close()

    def isOnline(self, host, port):
        result = self.sock.connect_ex((host, port))
        if result == 0:
            return True
        else:
            return False


def serve(connection, address, username, timeline, following):
    try:
        if DEBUG:
            print('> Connection from ', address)
        while True:
            data = connection.recv(1024)
            message = Protocol.Operation()
            message.ParseFromString(data)
            if data:
                process_message(message, connection, username, timeline, following)
            else:
                break
    finally:
        connection.close()


def process_message(message, connection, username, my_timeline, following):
    if type(message) is Protocol.Operation:
        if message.type == Protocol.GET_TIMELINE:
            if DEBUG:
                print(colored('\n> Received GET TIMELINE request.\n', 'blue'))

            timeline_username_target = message.username
            nr_messages = message.nr_messages

            if nr_messages > MAX_NR_MESSAGES:
                nr_messages = 10

            print(colored(f'> The number of requested messages is {nr_messages}.\n', 'blue'))

            timeline = []
            # The request is about my timeline
            if timeline_username_target == username:
                timeline = my_timeline[-nr_messages:]
            else:  # The request is about a user I follow
                following_timeline = [
                    following_peer for following_peer in following
                    if following_peer['username'] == timeline_username_target
                ][0]['timeline']
                timeline = following_timeline[-nr_messages:]

            # Create a reply msg and define the reply message type
            replyMessage = Protocol.OperationReply()
            replyMessage.type = Protocol.GET_TIMELINE
            replyMessage.username = timeline_username_target

            for timeline_post in timeline:
                # create a timeline post message
                timeline_post_message = replyMessage.timeline.add()
                timeline_post_message.id = timeline_post['id']
                timeline_post_message.content = timeline_post['content']
                timeline_post_message.timestamp = timeline_post['timestamp']

            connection.sendall(replyMessage.SerializeToString())
            print(colored(f'> Sent the requested timeline with success!.\n', 'green'))
        elif message.type == Protocol.PUBLISH:
            if DEBUG:
                print(colored('\n> Received BROADCAST request.\n', 'blue'))

            received_timeline = message.timeline
            publisher = message.username

            for timeline_post in received_timeline:
                # add to timeline
                followings_manager.add_msg_following(timeline_post.id, timeline_post.content, timeline_post.timestamp,
                                                     publisher, following)

            if DEBUG:
                print(colored('\n> Updated following timeline from publish with success.\n', 'green'))
                print(following)

            # Create a reply msg and define the reply message type
            replyMessage = Protocol.OperationReply()
            replyMessage.type = Protocol.ACK
            replyMessage.username = username

            connection.sendall(replyMessage.SerializeToString())
    elif type(message) is Protocol.OperationReply:
        if message.type == Protocol.GET_TIMELINE:
            timeline_username_target = message.username
            if DEBUG:
                print(colored(f'\n> Received GET TIMELINE from {timeline_username_target} reply message.\n', 'blue'))

            received_timeline = message.timeline

            for timeline_post in received_timeline:
                # add to timeline
                followings_manager.add_msg_following(timeline_post.id, timeline_post.content, timeline_post.timestamp,
                                                     timeline_username_target, following)
        elif message.type == Protocol.ACK:
            ack_user = message.username
            if DEBUG:
                print(colored(f'\n> Received ACK from {ack_user}.\n', 'blue'))
    else:
        if DEBUG:
            print(colored('\n> Received an unknown operation.\n', 'red'))
