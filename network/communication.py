from interface import interface
import json
import math
import random
import ntplib
from termcolor import colored
from datetime import datetime, timezone
from storage import followings_manager, user_manager
from protocol import protocol_pb2 as Protocol
from network.TCPConnection import TCPConnection

DEBUG = True


async def get_timeline(server, username, following, target):
    if username == target:
        print(colored('\n> You can\'t request your own timeline!\n', 'red'))
        interface.printMenu()
        return

    # Obtain from the DHT the information about the user I want to obtain the timeline
    value = await server.get(target)

    if value is None:
        print(colored(f'\n> User {target} not found in DHT.\n', 'blue'))
        interface.printMenu()
        return

    # Parse the obtained information
    userInfo = json.loads(value)

    vector_clocks = userInfo.get('vector_clock')

    # order by highest value which means order by highest clock
    vector_clocks_sorted_tuples = sorted(vector_clocks.items(), key=lambda x: x[1], reverse=True)
    vector_clocks_sorted_dict = {k: v for k, v in vector_clocks_sorted_tuples}
    highest_vector_clock = next(iter(vector_clocks_sorted_dict.values()))

    # obtain the current target following timeline
    target_timeline = [
        following_peer for following_peer in following if following_peer['username'] == target
    ][0]['timeline']

    target_current_local_max_clock = 0

    # determine the current max clock that I have from that following
    if target_timeline:
        target_current_local_max_clock = max(target_timeline, key=lambda x: x['id'])['id']

    if highest_vector_clock == target_current_local_max_clock:
        print(colored(f'\n> You already have the updated timeline from {target}. No need to request.\n', 'green'))
        interface.printMenu()
        return
    else:
        if DEBUG:
            print(colored(f'\n> It\'s necessary to update local timeline of the user {target} that I\'m following!\n'
                          f'> The current LOCAL vector clock of the user that I\'m following is: '
                          f'{target_current_local_max_clock} and the max vector clock that user has'
                          f' is: {highest_vector_clock}!\n', 'blue'))

        # filter peers by choosing the ones that have a higher vector clock than me
        filtered_peers = dict(
            filter(lambda follower: follower[1] > target_current_local_max_clock, vector_clocks_sorted_dict.items())
        )

        # obtain the port from an online peer that has the updated content based on my max clock from that peer
        port, online_peer_clock = await get_online_peer_port(userInfo['tcp_port'], target, userInfo['followers'], filtered_peers)

        if port is None:
            print(colored('\n> Can\'t get a online peer that has the content you requested based'
                          ' on your last clock from the user you are following!\n', 'red'))
            return

        timelineRequest = Protocol.Operation()
        timelineRequest.type = Protocol.GET_TIMELINE
        # set the current vector clock entry that I have from the target peer
        timelineRequest.nr_messages = online_peer_clock - target_current_local_max_clock
        # define the username from who I want to obtain the timeline
        timelineRequest.username = target

        tcp_connection = TCPConnection("localhost", port)
        tcp_connection.connect()
        tcp_connection.send_and_receive(timelineRequest.SerializeToString(), following)  # blocks until receive

        print(colored(f'> Get timeline from {target} was successful!', 'green'))

        if DEBUG:
            print([following_peer for following_peer in following if following_peer['username'] == target][0]['timeline'])

        # Set my vector clock to the online peer clock because now I have the updated timeline as him
        userInfo['vector_clock'][username] = online_peer_clock

        # Save in DHT
        await server.set(target, json.dumps(userInfo))
        print(colored(f'> Updated my vector clock in the entry of the following user in the DHT!', 'green'))


async def follow_user(server, username, user_to_follow, followings, tcp_connection):
    if username == user_to_follow:
        print(colored('\n> You can\'t follow yourself!\n', 'red'))
        interface.printMenu()
        return

    # Obtain from the DHT the information about the user I want to follow
    value = await server.get(user_to_follow)

    if value is None:
        print(colored('\n> User not found in DHT.\n', 'blue'))
        interface.printMenu()
        return

    # Parse the obtained information
    userInfo = json.loads(value)

    try:
        # Verify if the user I want to follow already has me in his followers list
        if userInfo['followers'][username]:
            print(colored('\n> Already following...\n', 'red'))
            interface.printMenu()
            return
    except Exception:
        # Add to the DHT entry of the user that I'm following my tcp port
        userInfo['followers'][username] = tcp_connection.getPort()
        userInfo['vector_clock'][username] = 0
        await server.set(user_to_follow, json.dumps(userInfo))
        # Save the following to my local following list
        followings_manager.add_following(user_to_follow, followings)
        print(colored(f'\n> Followed {user_to_follow} with success!\n', 'green'))
        print(colored(f'> Trying to update the user {user_to_follow} timeline...', 'blue'))
        await get_timeline(server, username, followings, user_to_follow)


async def publish(server, username, timeline, content):
    # Get Time from external source
    c = ntplib.NTPClient()
    response = c.request('pt.pool.ntp.org', version=3)
    time = datetime.fromtimestamp(response.tx_time, timezone.utc)

    # Save to local timeline
    timeline_post = user_manager.add_msg_timeline(content, timeline, time.__str__())

    if DEBUG:
        print(colored('> Saved to local timeline!', 'green'))
        print(f'\nTimeline: {timeline}')

    # Get list of subscribers
    value = await server.get(username)
    userInfo = json.loads(value)
    followers = userInfo['followers']

    # Increment publisher vector clock
    vc = userInfo['vector_clock'][username]
    userInfo['vector_clock'][username] = vc + 1

    # Save in DHT (reduce risk of overwrites)
    await server.set(username, json.dumps(userInfo))

    if DEBUG:
        print(colored("> User has " + str(len(followers)) + " followers", 'blue'))

    if len(followers) == 0:
        print(colored("> Not broadcasting to anyone.\n", 'yellow'))
        interface.printMenu()
        return

    # Send content over tcp to some subscribers (50%)
    n = math.ceil(len(followers) * 0.5)
    if DEBUG:
        print(colored("\n> Broadcasting to 50% of the followers -> " + str(n), 'green'))

    random_followers = random.sample(followers.keys(), k=n)

    for u in random_followers:
        if DEBUG:
            print(colored(f"\n> Trying to broadcast to peer {u}...", 'blue'))

        port = followers.get(u)

        tcp_connection = TCPConnection("localhost", port)
        if tcp_connection.isOnline("localhost", port):
            if DEBUG:
                print(colored(f'\n> Peer {u} is online, broadcasting...\n', 'green'))

            broadcast_message = Protocol.Operation()
            broadcast_message.type = Protocol.PUBLISH
            broadcast_message.username = username

            # create a timeline post message
            timeline_post_message = broadcast_message.timeline.add()
            timeline_post_message.id = timeline_post['id']
            timeline_post_message.content = timeline_post['content']
            timeline_post_message.timestamp = timeline_post['timestamp']

            # send the content over tcp
            tcp_connection.send_and_receive(broadcast_message.SerializeToString(), None)  # block until ACK

            # update vector clock of the user who acked
            userInfo['vector_clock'][u] = timeline_post['id']

            if DEBUG:
                print(colored(f'\n> Broadcast successful to peer {u}!\n', 'green'))
        else:
            if DEBUG:
                print(colored(f'\n> Peer {u} is offline...\n', 'red'))

    # Save in DHT
    await server.set(username, json.dumps(userInfo))
    print(colored(f'> Updated vector clocks entries in the DHT!\n', 'green'))
    interface.printMenu()


# Obtain the port from the node that is online and has the higher vector clock by passing a dict
# of possible peers, in this case possible peers are all that have higher vector clock than my
# local one from the user I am following
async def get_online_peer_port(user_tcp_port, target, target_followers, possible_peers):

    for user, clock in possible_peers.items():
        if user == target:
            port = user_tcp_port
        else:
            port = target_followers.get(user)

        tcp_connection = TCPConnection("localhost", port)

        if tcp_connection.isOnline("localhost", port):
            if DEBUG:
                print(colored(f'> Peer {user} is online and has the vector clock: {clock}.\n', 'green'))
            return port, clock
    return None
