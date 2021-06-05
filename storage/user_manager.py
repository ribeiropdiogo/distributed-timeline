# Functions for user's timeline
def add_msg_timeline(text, timeline, timestamp):
    number_id = len(timeline) + 1

    new_msg = ({'id': number_id, 'content': text, 'timestamp': timestamp})
    timeline.append(new_msg)
    return new_msg


def del_timeline_event(id_msg, timeline):
    for elem in timeline:
        if elem['id'] == id_msg:
            timeline.remove(elem)
    return timeline
