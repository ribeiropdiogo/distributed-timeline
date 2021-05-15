import argparse
import logging
import asyncio
from network import node
from storage import local_storage

#### Peer Global Variables ####
username  = ""
timeline  = []
following = []
###############################

def parse_arguments():
    parser = argparse.ArgumentParser()

    # Optional arguments
    parser.add_argument("-i", "--ip", help="IP address of existing node", type=str, default=None)
    parser.add_argument("-p", "--port", help="port number of existing node", type=int, default=None)
    parser.add_argument("-u", "--username", help="username of node", type=str, default="default")

    return parser.parse_args()

def main():
    args = parse_arguments()
    username = args.username

    # read the data from the local storage
    (timeline, following) = local_storage.read_data('database/example.yaml')
    if (timeline,following) != ([], []):
        print("> The imported data was:")
        print("\t- Timeline: " + str(timeline))
        print("\t- Following: " + str(following) + "\n")
    else:
        print("> No data was imported.\n")

    (server,loop) = node.start_node(args)

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
