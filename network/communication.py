from interface import interface
import json

async def get_timeline(server,username,target):
    value = await server.get(target)
    userInfo = json.loads(value)
    # Check if the user has updated content
    # If not, check the messages that are missing
    # Make TCP Request directly to target and ask for timeline
    # Save to local timeline
    return 0

async def follow_user(server,followingUser,followingUserPort,followedUser):
    value = await server.get(followedUser)
    #print(value)
    userInfo = json.loads(value)

    try:
        if userInfo['followers'][followingUser]:
            print("Already Following...")
    except Exception:
        userInfo['followers'][followingUser] = followingUserPort;
        userInfo['vector_clock'][followingUser] = 0;
        await server.set(followedUser,json.dumps(userInfo))
    
    interface.printMenu()

async def publish(server,username,content):
    # Save to local timeline
    # Get list of subscribers
    # Send content over tcp to some subscribers (50%)
    # (the users update vector clock on receive)
    return 0;
