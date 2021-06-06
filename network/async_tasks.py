import asyncio
import os

from termcolor import colored

from interface import interface
from network import communication

DEBUG = True

def printMessage(message):
    print(colored(message['username'], 'blue'), end=" ")
    print(colored(message['timestamp'], 'red'))
    print(colored(message['content'], 'green'))
    print('\n', end="")


def printFeed(timeline, following, user):
    toPrint = []
    for t in timeline:
        t['username'] = user
        toPrint.append(t)
    for f in following:
        for ti in f['timeline']:
            ti['username'] = f['username']
            toPrint.append(ti)
    toPrint.sort(reverse=True, key=lambda item: item.get("timestamp"))
    for m in toPrint:
        printMessage(m)


@asyncio.coroutine
def task(server, loop, username, tcp_connection, timeline, following, queue):
    interface.printMenu()
    while True:
        try:
            option = yield from queue.get()

            if option == 'exit':
                break

            if option == '1':
                os.system('cls' if os.name == 'nt' else 'clear')
                interface.followUser()
                # Get User To Follow
                user_to_follow = yield from queue.get()
                userInfo = {'username': username, 'following': following}
                # Follow User Function
                asyncio.create_task(communication.follow_user(
                    server, username, user_to_follow, following, tcp_connection,
                ))
            elif option == '2':
                os.system('cls' if os.name == 'nt' else 'clear')
                interface.publishContent()
                # Get Content to Publish
                content_to_publish = yield from queue.get()
                # Publish Content Function
                asyncio.create_task(communication.publish(
                    server, username, timeline, content_to_publish))
            elif option == '3':
                os.system('cls' if os.name == 'nt' else 'clear')
                result = get_followed_timelines(
                    server, username, following, loop)
                if result:
                    interface.feedHeader()
                    printFeed(timeline, following, username)
                # Show Feed Function
        except Exception:
            pass

    loop.call_soon_threadsafe(loop.stop)

def get_followed_timelines(server, username, following, loop):
    if not following:
        print(colored('> You are not following anyone...\n', 'red'))
        return False

    if DEBUG:
        print(colored('> Updating the timeline...', 'blue'))

    for user in following:
        following_username = user.get('username')
        if DEBUG:
            print(colored(
                f'> Trying to update the user {following_username} timeline...', 'blue'))
        loop.run_until_complete(communication.get_timeline(
            server, username, following, following_username))
    return True
