import os


class MongoConfig:
    def __init__(self):
        self.url = os.environ.get("MONGO_CONNECTION_URL", '10.216.247.82')
        self.db = os.environ.get("MONGO_DB", 'fusionconsumer')
        self.collection = os.environ.get("MONGO_COLLECTION", 'bulk_sync_user_active_data_migration')
        self.timeout = int(os.environ.get("MONGO_TIMEOUT", "1000"))

    def get_url(self):
        return self.url

    def get_db(self):
        return self.db

    def get_collection(self):
        return self.collection

    def get_timeout(self):
        return self.timeout
