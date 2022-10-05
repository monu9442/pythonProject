from app.repository.mongo import mongo_rep

mdb_data = mongo_rep.get_similar_profiles([79338312, 78893760])

for data in mdb_data:
    print(data)