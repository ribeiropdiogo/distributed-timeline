from interface import interface
import json

async def get_timeline(server,username,target):
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
    return 0;
