import time
import copy
from pprint import pprint
from request import new_request
import requests
import json
import timeit


class MakeApiCall:
    request_hit = {
    "express_resumes": {
        "size": 2,
        "from": 0
    },
    "size": 400,
    "recruiter_db_access_contexts": [
        "rexmonster"
    ],
    "from": 0,
    "sub_channel_id": 1,
    "recruiter_company_name": "Monster.com|Velankanni(pvt),corp.com",
    "subuid": 113486,
    "service_filter": {},
    "channel_id": 1,
    "corp_id": 10549,
    "site_context": "rexmonster",
    "filters": {
        "company": {
            "currency": "INR",
            "include_profiles_with_no_ctc": 1,
            "include_profiles_with_no_notice_period": 1,
            "any_scope": "c",
            "designations_scope": "c",
            "exclude_scope": "c"
        },
        "education": {
            "highest_second_cond": "AND",
            "yop_from": 0,
            "yop_to": 0
        },
        "location": {
            "current_preferred_location_cond": "AND"
        },
        "additional": {
            "show_active_created": "active",
            "active_created_days": 180
        }
    },
    "strict": True,
    "refine_search": {
        "sort_by": "relevance"
    },
    "queries": {
        "exclude_synonyms": 0,
        "search_within": "contents",
        "search_scope_id": 1,
        "any": "java"
    },
    "response_type": "seeker_services"}
    count = 0
    def get_user_data(self, api, parameters):
        response = requests.post(api, json=parameters)
        return response.json()

    def count_non_null_seekers(self, result):
        for doc in result:
            if doc['seeker_services'] is not None:
                self.count += 1

    def get_count_from_results(self):
        counter = 0
        while counter < 1741260:
            result = self.get_user_data("http://127.0.0.1:5000/search", self.request_hit)
            self.count_non_null_seekers(result['all_resumes'])
            self.request_hit['from'] = self.request_hit['from'] + self.request_hit['size']
            counter += self.request_hit['size']



api_call = MakeApiCall()
api_call.get_count_from_results()


