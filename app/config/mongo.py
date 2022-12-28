import os

MONGO_URL = 'polaris'

class MongoConfig:
    def __init__(self):
        self.url = MONGO_URL
        self.db = os.environ.get("MONGO_DB", "resumes")
        self.collection = os.environ.get("MONGO_COLLECTION")
        self.timeout = int(os.environ.get("MONGO_TIMEOUT", "1000"))
    


    def get_url(self):
        return self.url

    def get_db(self):
        return self.db

    def get_collection(self):
        return self.collection

    def get_timeout(self):
        return self.timeout


mongo_config = MongoConfig()