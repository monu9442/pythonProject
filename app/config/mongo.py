import os

class MongoConfig:
    def __init__(self):
        self.url = os.environ.get("MONGO_CONNECTION_URL","mongodb://polaris:polaris@10.216.247.81/recruiters" )
        self.db = os.environ.get("MONGO_DB", "resumes")
        self.collection = os.environ.get("MONGO_COLLECTION", 'seeker_resumes')
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