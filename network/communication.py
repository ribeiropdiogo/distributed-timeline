from interface import interface
import json
import math
import random
import ntplib
from termcolor import colored
from datetime import datetime, timezone
from protocol import protocol_pb2 as Protocol
from network.TCPConnection import TCPConnection

DEBUG = True

async def get_timeline(server, username, timeline, target):

    if username == target:
        print(colored('\n> You can\'t request your own timeline!\n', 'red'))
        interface.printMenu()
        return

    port = await get_online_peer_port(server, username, target)

    timelineRequest = Protocol.Operation()
    timelineRequest.type = Protocol.GET_TIMELINE;

    tcp_connection = TCPConnection("localhost", port)
    tcp_connection.connect()
    tcp_connection.send_and_receive(timelineRequest.SerializeToString(), timeline)

    # Check if the user has updated content
    # If not, check the messages that are missing
    # Make TCP Request directly to target and ask for timeline
    # Save to local timeline
    interface.printMenu()
    return 0

async def follow_user(server, localUserInfo, tcp_connection, userToFollow):
    
    if localUserInfo['username'] == userToFollow:
        print(colored('\n> You can\'t follow yourself!\n', 'red'))
        interface.printMenu()
        return

    # Obtain from the DHT the information about the user I want to follow
    value = await server.get(userToFollow)
    
    if value is None:
        print(colored('\n> User not found in DHT.\n', 'blue'))
        interface.printMenu()
        return

    # Parse the obtained information
    userInfo = json.loads(value)

    try:
        # Verify if the user I want to follow already has me in his followers list
        if userInfo['followers'][localUserInfo['username']]:
            print(colored('\n> Already following...\n', 'red'))
    except Exception:
        # Add to the DHT entry of the user that I'm following my tcp port
        userInfo['followers'][localUserInfo['username']] = tcp_connection.getPort();
        userInfo['vector_clock'][localUserInfo['username']] = 0;
        await server.set(userToFollow,json.dumps(userInfo))
        # Save the following to my local following list
        localUserInfo['following'].append({'username': userToFollow})
        print(colored(f'\n> Followed {userToFollow} with success!\n', 'green'))
    interface.printMenu()

async def publish(server,localUserInfo,content,tcp_connection):
    # Get Time from external source
    c = ntplib.NTPClient()
    response = c.request('pt.pool.ntp.org', version=3)
    response.offset
    time = datetime.fromtimestamp(response.tx_time, timezone.utc)
    print(time)

    username = localUserInfo['username']
    localTimeline = localUserInfo['timeline']

    # Save to local timeline
    localTimeline.append({})

    # Get list of subscribers
    value = await server.get()
    userInfo = json.loads(value)
    followers = userInfo['followers']

    # Increment publisher vector clock
    vc = userInfo['vector_clock'][username]
    userInfo['vector_clock'][username] = vc + 1 
    print(userInfo['vector_clock'][username])

    # Save in DHT (reduce risk of overwrites)
    await server.set(username,json.dumps(userInfo))

    if DEBUG:
        print("> User has " + str(len(followers)) + " followers")

    # Send content over tcp to some subscribers (50%)
    n = math.ceil(len(followers) * 0.5)
    if DEBUG:
        print("> Broadcasting to 50% -> " + str(n))
    
    random_followers = random.sample(followers.keys(), k = n)

    for u in random_followers:
        if DEBUG:
            print(u + " - " + str(followers.get(u)))
        # send the content over tcp
        msg = "set " + username + " " + content
        tcp_connection.send('127.0.0.1',followers.get(u),msg)

    # (the users update vector clock on receive)

    interface.printMenu()


# Obtain the port from the node that is online and has the higher vector clock
async def get_online_peer_port(server, username, target):
    # Obtain from the DHT the information about the user I want to obtain the timeline
    value = await server.get(target)

    if value is None:
       print(colored('\n> User not found in DHT.\n', 'blue'))
       interface.printMenu()
       return
    
    # Parse the obtained information
    userInfo = json.loads(value)

    print(userInfo)

    return userInfo['tcp_port']

    # Obtain the target followers vector clocks
    #targetFollowersVectorClocks = userInfo['vector_clock']
    #print(targetFollowersVectorClocks)

    # Obtain the users with the highest vector clock
    #targetFollowersVectorClocks.

    connection_info = []
    result = await server.get(nickname)

    if result is None:
        print('ERROR - Why don\'t I belong to the DHT?')
    else:
        userInfo = json.loads(result)
        print(userInfo)
        userInfo['vector_clock'][nickname] += 1
        vector_clock[nickname] += 1
        await server.set(nickname, json.dumps(userInfo))
        for user, info in userInfo['followers'].items():
            connection_info.append(info)
    return connection_info