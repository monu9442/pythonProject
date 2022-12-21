from datetime import datetime
import pymongo
from pymongo.errors import AutoReconnect
from app.config.mongo import mongo_config


class MongoUtil:
    def create_connection(self):
        try:
            self.__mongo_connection = pymongo.MongoClient(self.properties.get_url(),
                                                          serverSelectionTimeoutMS=self.properties.get_timeout())
            self.__mongo_collection = self.__mongo_connection[self.properties.get_db()][
                self.properties.get_collection()]

        except Exception as error_in_connection:
            print(f"Error in Creating Connection : {error_in_connection}")

    def __init__(self):
        self.properties = mongo_config
        self.__mongo_connection = None
        self.__mongo_collection = None
        self.create_connection()

    def insert_data(self, data):
        try:
            self.__mongo_collection.insert_many(data) # data is a list containing data to be inserted
        except Exception as e:
            print("Error Occurred in inserting data in MongoDB.........")

    def get_data(self, query):
        return self.__mongo_collection.find(query)

    def get_single_profile(self, query):
        return self.__mongo_collection.find_one(query)




mongo_util = MongoUtil()
