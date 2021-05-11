import argparse
import logging
import asyncio

from kademlia.network import Server

DEBUG = True
BOOTSTRAP_NODE = 8468

def start_node(args):
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    if DEBUG:
        log = logging.getLogger('kademlia')
        log.addHandler(handler)
        log.setLevel(logging.DEBUG)

    server = Server()

    loop = asyncio.get_event_loop()

    if DEBUG:
        loop.set_debug(True)

    if args.ip and args.port:
        loop.run_until_complete(server.listen(int(args.port)))
        bootstrap_node = (args.ip, BOOTSTRAP_NODE)
        loop.run_until_complete(server.bootstrap([bootstrap_node]))
    else:
        loop.run_until_complete(server.listen(BOOTSTRAP_NODE))

    return (server,loop)