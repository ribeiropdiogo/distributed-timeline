import asyncio
import os
from interface import interface
from network import communication

@asyncio.coroutine
def task(server, loop, username, tcp_port, timeline, following, queue):
    interface.printMenu()
    while True:
        input = yield from queue.get()
        
        if input == 'exit':
            break
        
        if(input == '1'):
            os.system('cls' if os.name == 'nt' else 'clear')
            interface.followUser()
            # Get User To Follow
            input = yield from queue.get()
            # Follow User Function
            asyncio.create_task(communication.follow_user(server,username,tcp_port,input))
            #loop.run_until_complete(communication.get_timeline(server,username,input))
        elif(input == '2'): 
            os.system('cls' if os.name == 'nt' else 'clear')
            interface.publishContent() 
            # Get Content to Publish
            input = yield from queue.get()
            # Publish Content Function
            loop.run_until_complete(communication.publish(server,username,input))
        elif(input == '3'): 
            os.system('cls' if os.name == 'nt' else 'clear')
            get_followed_timelines(server,username,following,loop)
            interface.feedHeader() 
            # Show Feed Function

    loop.call_soon_threadsafe(loop.stop)
        
def get_followed_timelines(server,username,following,loop):
    # Para cada user seguido, efetuar pedido
    for user in following:
        print(user)
        #loop.run_until_complete(communication.get_timeline(server,username,user))
