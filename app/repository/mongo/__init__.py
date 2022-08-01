from app.utils.mongo_database import connector
from app.repository.mongo.profile import profile
import os

class mongo():
   def execute_query(self, query):
       collection = os.environ.get('MDB_COLLECTION_NAME')
       database = os.environ.get('MDB_NAME')
       db_data = connector.client[database][collection].find(query)
       return db_data



