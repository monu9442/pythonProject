class Profile:

    def get_profile(self, profile_id = None):
        if not profile_id:
            return{}
        return {'country': profile_id }

    def get_profile_gte(self, profile_id_threshold):
        if not profile_id_threshold:
            return {}
        return {'year':{'$gte': profile_id_threshold}}


profile = Profile()
