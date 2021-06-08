import argparse
import asyncio
import time
import os
from termcolor import colored
from network.TCPConnection import TCPConnection
from network import communication
from network import node, dhtUserInfo
from storage import local_storage
from threading import Thread

# ---- Peer Global Variables ---- #
username = ""
timeline = []
following = []
tcp_port = 1337
test_arg = None
##################################


def parse_arguments():
    parser = argparse.ArgumentParser()

    # Optional arguments
    parser.add_argument("-i", "--ip", help="IP address of existing node", type=str, default="localhost")
    parser.add_argument("-p", "--port", help="port number of existing node", type=int, default=None)
    parser.add_argument("-tcp", "--tcp_port", help="tcp port number of existing node", type=int, default=1337)
    parser.add_argument("-u", "--username", help="username of node", type=str, default="bootstrap")
    parser.add_argument("-t", "--test", help="test", type=int, default=None)

    return parser.parse_args()


async def insertUserDHT(server, username, port, max_clock):
    exists = await server.get(username)
    if exists is None:
        user_info = dhtUserInfo.create(username, port, max_clock)
        await server.set(username, user_info)
    else:
        print("> User present in DHT")


# Launch TCP Connection for peer messaging
def launchTCP(connection, username, timeline, following):
    connection.bind()
    connection.listen(username, timeline, following)


async def async_tasks(server, loop, username, tcp_connection, timeline, following):
    num_iterations = 100

    time.sleep(5)

    await communication.follow_user(server, username, f"user{test_arg}", following, tcp_connection)

    time.sleep(5)

    response_times = []
    start_ns = time.time_ns()

    for _ in range(num_iterations):
        op_start_ns = time.time_ns()

        #await communication.follow_user(server, username, "luis", following, tcp_connection)
        await communication.publish(server, username, timeline, "tweet")
        #await communication.get_timeline(server, username, following, "luis")
        
        op_end_ns = time.time_ns()
        response_times.append((op_end_ns-op_start_ns)/1_000_000)

    end_ns = time.time_ns()
    time_s = (end_ns-start_ns) / 1_000_000_000
    num_ops = len(response_times)
    ops_per_sec = num_ops / time_s
    results = [num_ops, time_s, ops_per_sec, min(response_times), max(response_times), sum(response_times)/num_ops]
    print(f'\nresults: {results}\n', flush=True)

    while True:
        time.sleep(1)

    loop.call_soon_threadsafe(loop.stop)


def main():
    args = parse_arguments()
    username = args.username
    tcp_port = args.tcp_port
    global test_arg
    test_arg = args.test

    tcp_connection = None
    task = None

    # Connect node to network
    (server, loop) = node.start_node(args)

    if username != "bootstrap":
        # read the data from the local storage
        (timeline, saved_following) = local_storage.read_data(f'database/{username}.yaml')

        if (timeline, saved_following) != ([], []):
            print("> The imported data was:")
            print("\t- Timeline: " + str(timeline))
            print("\t- Following: " + str(saved_following) + "\n")
            for following_user in saved_following:
                following_user['timeline'] = []
        else:
            print("> No data was imported.\n")

        print(colored(f'\n> Peer {username} started!\n', 'blue'))

        following = []

        # Start connection to communicate with other nodes directly and pass to thread
        tcp_connection = TCPConnection(args.ip, tcp_port)
        thread = Thread(target=launchTCP, args=(tcp_connection, username, timeline, following))
        thread.start()

        # Initialize User in DHT
        max_clock = 0
        if timeline:
            max_clock = max(timeline, key=lambda x: x['id'])['id']
        loop.run_until_complete(insertUserDHT(server, username, tcp_port, max_clock))

        # Recover from reboot, iterate through followings and ask for timeline
        #print(saved_following)
        #if saved_following:
        #    for saved_following_user in saved_following:
        #        loop.run_until_complete(communication.follow_user(
        #                server, username, saved_following_user['username'], following, tcp_connection
        #            )
        #        )

        # Build CLI Menu for user to interact
        task = asyncio.run_coroutine_threadsafe(
            async_tasks(server, loop, username, tcp_connection, timeline, following), loop
        )
    else:
        print(colored(f'\n> Bootstrap node started!\n', 'blue'))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        if username != 'bootstrap':
            print(colored('\n> Peer is closed!', 'blue'))
            print(f'\nFollowing: {following}')
            print(f'\nTimeline: {timeline}')
            local_storage.save_data(timeline, following, username)  # save all info about this peer in the local storage
            print(colored('\n> All data was saved!', 'green'))
            task.cancel()
            tcp_connection.close()
        else:
            print(colored('\n> Bootstrap node closed!', 'blue'))
        server.stop()
        loop.close()


if __name__ == "__main__":
    main()
