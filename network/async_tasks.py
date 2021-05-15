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

        #para limpar o ecrã dps
        #os.system('cls' if os.name == 'nt' else 'clear')
        interface.printMenu()
    loop.call_soon_threadsafe(loop.stop)

def parseOption(option):                          
    if(option == '1\n'):
        print("opção 1 ")
    elif(option == '2\n'):  
        print("opção 2 ")      