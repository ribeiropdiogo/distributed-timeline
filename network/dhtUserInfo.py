import json


def create(username, port):
    userInfo = {
        "tcp_port": port,
        "followers": {},
        "vector_clock": {
            username: 0
        }
    }
    return json.dumps(userInfo)
