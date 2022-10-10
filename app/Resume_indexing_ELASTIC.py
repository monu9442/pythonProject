from pymongo import MongoClient
from elasticsearch import Elasticsearch
from tqdm import tqdm
file = open('profile_id_list.txt', 'w+')

MDB_CLIENT = MongoClient("mongodb://akhileshn:akhileshn@10.216.247.81/?authMechanism=DEFAULT&authSource"
                         "=similar_profiles")

es_QA = Elasticsearch('http://10.216.247.150/')
es_prod = Elasticsearch(['http://172.30.28.46:9200', 'http://172.30.28.47:9200'], maxsize=25, timeout=120,http_auth=('readonly', 'readonly'))

doc = {
    'profile_id': 124,
    'resume_text': 'This is a sample text to index to Elastic_search'
}

profile_query = {"query": {
  "match": {
    "profile_id": ""
  }
}}

collection = MDB_CLIENT["resumes"]["seeker_resumes"]
db_data = collection.find({}, batch_size=500)
count = 0
profile_id_list = []
for data in db_data:
     profile_id_list.append(data['profile_id'])
print(count)
file.write(str(profile_id_list))
failed_id_list = []

for data in db_data:
    profile_id = data['profile_id']

    final_document = dict()
    profile_query['query']['match']['profile_id'] = profile_id
    prod_profile = es_prod.search(index='livecore_india', body= profile_query)

    if prod_profile['hits']['total']['value'] > 0:
        final_document = prod_profile['hits']['hits'][0]['_source']
        final_document['resume_text'] = data['resume_text']
        resp = es_QA.index(index="resume_text_db", document=final_document)
        print(resp['result'])
    else:
        failed_id_list.append(profile_id)
        print(f"No profile for id : {profile_id} on Elastic Production")

file.write(str(failed_id_list))
print("Task Finished........")