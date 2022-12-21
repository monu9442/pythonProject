from app.utils.mongo import mongo_util


class MongoRepository:
    similar_profiles_query = {"falconUserId": {"$in": []}}

    profile_query = {"profile_id": ""}

    def get_similar_profiles(self, profile_ids):
        query = self.similar_profiles_query
        query["falconUserId"]['$in'] = profile_ids
        mdb_data = mongo_util.get_data(query)
        return mdb_data

    def get_profile(self, profile_id):
        query = self.profile_query
        query['profile_id'] = profile_id
        mdb_data = mongo_util.get_single_profile(query)
        return mdb_data

mongo_rep = MongoRepository()
