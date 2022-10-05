from app.utils.mongo import mongo_util


class MongoRepository:
    similar_profiles_query = {"falconUserId": {"$in": []}}

    def get_similar_profiles(self, profile_ids):
        query = self.similar_profiles_query
        query["falconUserId"]['$in'] = profile_ids
        mdb_data = mongo_util.get_data(query)
        return mdb_data


mongo_rep = MongoRepository()
