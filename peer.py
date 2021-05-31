import argparse
from asyncio.tasks import sleep
import logging
import asyncio
from network.TCPConnection import TCPConnection
import sys
import signal
from network import node, async_tasks, communication, dhtUserInfo
from storage import local_storage
from threading import Thread

#### Peer Global Variables ####
username  = ""
timeline  = []
following = []
inputs = asyncio.Queue()
tcp_port = 1337
###############################

def handle_user_input():
    data = sys.stdin.readline()
    asyncio.gather(inputs.put(data.rstrip()))

def parse_arguments():
    parser = argparse.ArgumentParser()

    # Optional arguments
    parser.add_argument("-i", "--ip", help="IP address of existing node", type=str, default="localhost")
    parser.add_argument("-p", "--port", help="port number of existing node", type=int, default=None)
    parser.add_argument("-tcp", "--tcp_port", help="tcp port number of existing node", type=int, default=1337)
    parser.add_argument("-u", "--username", help="username of node", type=str, default="bootstrap")

    return parser.parse_args()

async def insertUserDHT(server,username,port):
    exists = await server.get(username)
    if exists is None:
        user_info = dhtUserInfo.create(username,port)
        await server.set(username, user_info)
    else:
        print("> User present in DHT")

# Launch TCP Connection for peer messaging
def launchTCP(connection,username, timeline):
    connection.bind()
    connection.listen(username, timeline)

def main():
    args = parse_arguments()
    username = args.username
    tcp_port = args.tcp_port

    # Connect node to network
    (server,loop) = node.start_node(args)

    # read the data from the local storage
    #(timeline, following) = local_storage.read_data(f'database/{username}.yaml')
    '''
    if (timeline,following) != ([], []):
        print("> The imported data was:")
        print("\t- Timeline: " + str(timeline))
        print("\t- Following: " + str(following) + "\n")
    else:
        print("> No data was imported.\n")
    '''

    if username != "bootstrap":
        # Start connection to communicate with other nodes directly and pass to thread
        tcp_connection = TCPConnection(args.ip, tcp_port)
        thread = Thread(target = launchTCP, args = (tcp_connection,username,timeline))
        thread.start()


    # User Input Handling
    loop.add_reader(sys.stdin, handle_user_input)

    if username != "bootstrap":

        # TODO
        # Recover from reboot, iterate through followings and ask for timeline
        if following != []:
            print()

        # Initialize User in DHT
        loop.run_until_complete(insertUserDHT(server,username,tcp_port))


    # Build CLI Menu for user to interact
    if username != "bootstrap":
        task = asyncio.run_coroutine_threadsafe(async_tasks.task(server, loop, username, tcp_connection, timeline, following,inputs), loop) 
    
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:                   
        print("\n> Peer is closed!")
        print(following)
        local_storage.save_data(timeline, following, username) # save all info about this peer in the local storage
        print('\n> All data was saved!')
        server.stop()
        tcp_connection.close()
        loop.close()

if __name__ == "__main__":
    main()
