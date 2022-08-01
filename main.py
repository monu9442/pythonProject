from app.repository.mongo import mongo
from app.repository.mongo import profile

Mongo_data_fetcher = mongo()
doc_id = 'Russia'
documents = Mongo_data_fetcher.execute_query(profile.get_profile(doc_id))

for data in documents:
    print(data.get('country'))
