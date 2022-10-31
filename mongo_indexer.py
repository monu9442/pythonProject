from app.repository.mongo import mongo_rep
from app.profile_id import profile_id_list
from pymongo.mongo_client import MongoClient


client = MongoClient("mongodb://polaris:polaris@10.216.247.81/recruiters")
collection = client["resumes"]["clean_text_resumes"]

query = {"source_profile_ids"}
query_1 = {"profile_id" : {"$in":[67674514]} }
id_list = []
mdb_data = collection.find(query_1)

for data in mdb_data:
    if data.get("profile_id") in id_list:
        continue
    id_list.append(data.get("profile_id"))
    print(data)