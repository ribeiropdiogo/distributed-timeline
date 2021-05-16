import asyncio
import os
from interface import interface

@asyncio.coroutine
def task(server, loop, username, queue):
    interface.printMenu()
    while True:
        input = yield from queue.get()

        if input == 'exit\n':
            break

        parseOption(input)
        interface.printMenu()
    loop.call_soon_threadsafe(loop.stop)

def parseOption(option):                          
    if(option == '1\n'):
        os.system('cls' if os.name == 'nt' else 'clear')
        interface.followUser()
        # Follow User Function
    elif(option == '2\n'):  
        os.system('cls' if os.name == 'nt' else 'clear')
        interface.publishContent() 
        # Publish Content Function
    elif(option == '3\n'):  
        os.system('cls' if os.name == 'nt' else 'clear')
        interface.feedHeader() 
        # Show Feed Function
