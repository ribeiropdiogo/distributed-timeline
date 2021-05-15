import asyncio
import os
from interface import interface

@asyncio.coroutine
def task(server, loop, username, queue):
    interface.printMenu()
    while True:
        msg = yield from queue.get()
        if msg == 'exit\n':
            break

        os.system('cls' if os.name == 'nt' else 'clear')
        interface.printMenu()
    loop.call_soon_threadsafe(loop.stop)

def cancel_task():                          
    for task in asyncio.all_tasks():
        task.cancel()                   