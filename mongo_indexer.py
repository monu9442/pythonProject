from app.repository.mongo import mongo_rep
from app.profile_id import profile_id_list
from pymongo.mongo_client import MongoClient


MDB_DEST = MongoClient("mongodb://polaris:polaris@10.216.247.81/recruiters")
DEST_COLL = MDB_DEST['resumes']['clean_text_resumes']

if DEST_COLL.find_one({"profile_id":101633666}):
    DEST_COLL.update_many({"profile_id":101633666},{"$set":{"profile_id":101633666,"resume_text": "This is a sample update "
                                                                                         "filter text"}},upsert=True)
