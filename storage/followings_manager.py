N = 10  # number of messages stored by following


def add_following(username, followings):
    new_following = {
        "username": username,
        "timeline": []
    }

    followings.append(new_following)


def get_following(username, followings):
    for fol in followings:
        if fol['username'] == username:
            return True, fol

    return False, {}


def del_following(username, followings):
    for fol in range(len(followings)):
        if followings[fol]['username'] == username:
            del followings[fol]
            break


def add_msg_following(msg_id, content, timestamp, username, followings):
    (exists, fol) = get_following(username, followings)
    if exists:
        if 'timeline' not in fol:
            fol['timeline'] = []

        fol['timeline'].append(dict({'id': msg_id,
                                     'content': content,
                                     'timestamp': timestamp
                                     }))
        if len(fol['timeline']) > N:
            del_msg_following(username, followings)
        return True

    return False


# remove messages from a following's timeline
# in his timeline will remain the N most recent messages
def del_msg_following(identity, followings):
    (b, fol) = get_following(identity, followings)

    if b:
        if len(fol['timeline']) == 0:
            return 0
        else:
            list_msg = fol['timeline']
            tam = len(list_msg)

            if tam > N:
                [list_msg.remove(list_msg[i]) for i in range(0, (tam - N) + 1)]
                return tam - N

            else:
                return 0

    else:
        return 0
