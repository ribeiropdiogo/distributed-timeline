import argparse
import logging
import asyncio
from network import node

#### Peer Global Variables ####
username  = ""
following = []
timeline  = []
###############################

def parse_arguments():
    parser = argparse.ArgumentParser()

    # Optional arguments
    parser.add_argument("-i", "--ip", help="IP address of existing node", type=str, default=None)
    parser.add_argument("-p", "--port", help="port number of existing node", type=int, default=None)
    parser.add_argument("-u", "--username", help="username of node", type=str, default=None)

    return parser.parse_args()

def main():
    args = parse_arguments()
    username = args.username
    (server,loop) = node.start_node(args)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()
        loop.close()

if __name__ == "__main__":
    main()
