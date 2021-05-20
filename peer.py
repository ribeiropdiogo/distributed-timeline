import argparse
from asyncio.tasks import sleep
import logging
import asyncio
import sys
import signal
from network import node, async_tasks, communication
from storage import local_storage
from threading import Thread

#### Peer Global Variables ####
username  = ""
timeline  = []
following = []
inputs = asyncio.Queue()
###############################

def handle_user_input():
    data = sys.stdin.readline()
    asyncio.gather(inputs.put(data.rstrip()))

def parse_arguments():
    parser = argparse.ArgumentParser()

    # Optional arguments
    parser.add_argument("-i", "--ip", help="IP address of existing node", type=str, default=None)
    parser.add_argument("-p", "--port", help="port number of existing node", type=int, default=None)
    parser.add_argument("-u", "--username", help="username of node", type=str, default="default")

    return parser.parse_args()

async def insertUserDHT(server):
    exists = await server.get(str(username))
    if exists is None:
        user_info = "uelele"
        await server.set(str(username), user_info)
    else:
        print("> User present in DHT")

def main():
    args = parse_arguments()
    username = args.username

    # Connect node to network
    (server,loop) = node.start_node(args)

    # read the data from the local storage
    (timeline, following) = local_storage.read_data('database/example.yaml')
    '''
    if (timeline,following) != ([], []):
        print("> The imported data was:")
        print("\t- Timeline: " + str(timeline))
        print("\t- Following: " + str(following) + "\n")
    else:
        print("> No data was imported.\n")
    '''

    # Start connection to communicate with other nodes directly and pass to thread


    # User Input Handling
    loop.add_reader(sys.stdin, handle_user_input)

    if username != "default":
        # Initialize User in DHT
        loop.run_until_complete(insertUserDHT(server))


    # Build CLI Menu for user to interact
    task = asyncio.run_coroutine_threadsafe(async_tasks.task(server, loop, username, timeline, following,inputs), loop) 
    
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:                   
        print("\n> Peer is closed!")
        local_storage.save_data(timeline, following, username) # save all info about this peer in the local storage
        print('\n> All data was saved!')
        server.stop()
        loop.close()

if __name__ == "__main__":
    main()
