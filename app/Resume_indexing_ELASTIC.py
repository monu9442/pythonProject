from pymongo import MongoClient
from elasticsearch import Elasticsearch

MDB_CLIENT = MongoClient("mongodb://akhileshn:akhileshn@10.216.247.81/?authMechanism=DEFAULT&authSource"
                         "=similar_profiles")

es = Elasticsearch('http://10.216.247.150/')

doc = {
    'profile_id': 124,
    'resume_text': 'This is a sample text to index to Elastic_search'
}

resp = es.index(index="resume_text_db", document=doc)
print(resp['result'])

collection = MDB_CLIENT["resumes"]["seeker_resumes"]
db_data = collection.find()

for data in db_data:
    doc['profile_id'] = data["profile_id"]
    doc['resume_text'] = data['resume_text']
    resp = es.index(index="resume_text_db", document=doc)
    print(resp['result'])
