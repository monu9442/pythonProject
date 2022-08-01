import pymongo
from config.database import DbCredentials

class MDbConnector:
    def __init__(self, credentials):
        self.credentials = credentials
        self.client = self.create_connections()

    def create_connections(self):
        try:
            client = pymongo.MongoClient(self.credentials)
            return client
        except:
            with Exception as Error:
                print(f'Error Occured : {Error}')


connector = MDbConnector(DbCredentials.mongo)






