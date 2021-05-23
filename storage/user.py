from datetime import timezone
import datetime


def current_time_utc():
    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()        

    return utc_timestamp


# Functions for user's timeline
def add_msg_timeline(text, timeline):
    number_id = len(timeline) + 1
  
    if len(timeline) == 0:
        timeline = []

    timestamp = current_time_utc()
    new_msg = ({'id': number_id, 'content': text, 'timestamp': timestamp})
    timeline.append(new_msg)

def del_timeline_event(id_msg, timeline):
    for elem in timeline:
        if elem['id'] == id_msg:
           timeline.remove(elem)