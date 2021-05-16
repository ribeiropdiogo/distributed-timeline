#Add someone to follow
def add_following(identity, username, ip, port, following):
    new_following = ({'identity': identity, 'username': username, 
                    'ip': ip, 'port': port, 'track_timeline': 0})

    following.append(new_following)

def get_one_following(identity, following):
    for fol in following:    
        if fol['identity'] == identity:
            return (True, fol)

    return (False, {})

def del_following(identity, following):
    for fol in range(len(following)):
        if following[fol]['identity'] == identity:
           del following[fol]
           break

def add_msg_following_timeline(msg_id, content, identity, following):
    (b, fol) = get_one_following(identity, following)
    
    if b == True:
        if 'timeline' not in fol:
            fol['track_timeline'] = 0
            fol['timeline'] = []
        
        if fol['track_timeline'] == msg_id - 1:
            fol['track_timeline'] = msg_id
            fol['timeline'].append(dict({'id': msg_id, 'content': content}))
            return True

    return False

#remove n first messages from a following's timeline
# in his timeline will remain the most recent messages and 
# the track_timeline will store the last id_message received
def del_msg_following_timeline(n_msg, identity, following):
    (b, fol) = get_one_following(identity, following)

    if b == True:
        i = 0
        if 'timeline' not in fol:
            return i
        else:
            list_msg = fol['timeline']
        
        if n_msg > fol['track_timeline']:
            n_msg = fol['track_timeline']
        
        while n_msg > 0:
            del list_msg[0]
            n_msg -=1
            i +=1
        
        return i
    
    else: return 0


# Functions for user's timeline
def add_msg_my_timeline(text, timeline):
    number_id = len(timeline) + 1

    if len(timeline) == 0:
        timeline = []

    new_msg = ({'id': number_id, 'content': text})

    timeline.append(new_msg)

def del_timeline_event(id_msg, timeline):
    for elem in timeline:
        if elem['id'] == id_msg:
           timeline.remove(elem)
