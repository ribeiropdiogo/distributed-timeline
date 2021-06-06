import json


def create(username, port, max_clock):
    userInfo = {
        "tcp_port": port,
        "followers": {},
        "vector_clock": {
            username: max_clock
        }
    }
    return json.dumps(userInfo)
