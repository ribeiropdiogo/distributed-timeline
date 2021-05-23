from interface import interface
import json
import math
import random
import ntplib
from datetime import datetime, timezone

DEBUG = True

async def get_timeline(server,username,target):
    value = await server.get(target)
    userInfo = json.loads(value)
    # Check if the user has updated content
    # If not, check the messages that are missing
    # Make TCP Request directly to target and ask for timeline
    # Save to local timeline
    return 0

async def follow_user(server,followingUser,tcp_connection,followedUser):
    value = await server.get(followedUser)
    #print(value)
    userInfo = json.loads(value)

    try:
        if userInfo['followers'][followingUser]:
            print("Already Following...")
    except Exception:
        userInfo['followers'][followingUser] = tcp_connection.getPort();
        userInfo['vector_clock'][followingUser] = 0;
        await server.set(followedUser,json.dumps(userInfo))
    
    interface.printMenu()

async def publish(server,username,content,tcp_connection):
    # Get Time from external source
    c = ntplib.NTPClient()
    response = c.request('pt.pool.ntp.org', version=3)
    response.offset
    time = datetime.fromtimestamp(response.tx_time, timezone.utc)
    print(time)

    # Save to local timeline
    # ...

    # Get list of subscribers
    value = await server.get(username)
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
