import os


class Queue:
    host = None
    port = None
    user = None
    password = None

    def __init__(self):
        self.host = os.environ.get("QUEUE_HOST")
        self.port = os.environ.get("QUEUE_PORT")
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
