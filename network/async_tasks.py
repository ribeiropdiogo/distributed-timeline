import asyncio
import os
from interface import interface
from network import communication

@asyncio.coroutine
def task(server, loop, username, tcp_connection, timeline, following, queue):
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
            userInfo = {'username': username, 'following': following}
            # Follow User Function
            asyncio.create_task(communication.follow_user(server, userInfo, tcp_connection, input))
            #loop.run_until_complete(communication.get_timeline(server,username,input))
        elif(input == '2'): 
            os.system('cls' if os.name == 'nt' else 'clear')
            interface.publishContent() 
            # Get Content to Publish
            input = yield from queue.get()
            userInfo = {'username': username, 'timeline': timeline}
            # Publish Content Function
            asyncio.create_task(communication.publish(server, userInfo, input, tcp_connection))
        elif(input == '3'): 
            os.system('cls' if os.name == 'nt' else 'clear')
            get_followed_timelines(server, username, following, timeline, loop)
            interface.feedHeader() 
            # Show Feed Function

    loop.call_soon_threadsafe(loop.stop)
        
def get_followed_timelines(server, username, following, timeline, loop):
    # Para cada user seguido, efetuar pedido
    #for user in following:
        #print(user)
        loop.run_until_complete(communication.get_timeline(server, username, timeline,'joao'))
