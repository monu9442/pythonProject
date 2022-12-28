import os
QUEUE_PORT = '5672'

# QA
QUEUE_HOST = '172.30.3.42'

# PROD
# QUEUE_HOST = '172.30.25.10'


class Queue:
    host = None
    port = None
    user = None
    password = None

    def __init__(self):
        self.host = QUEUE_HOST
        self.port = QUEUE_PORT
        self.user = os.environ.get("QUEUE_USER")
        self.password = os.environ.get("QUEUE_PASSWORD")

    def get_host(self):
        return self.host

    def get_port(self):
        return self.port

    def get_user(self):
        return self.user

    def get_password(self):
        return self.password


QueueCredentials = Queue()
