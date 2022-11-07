import time
import copy
from pprint import pprint
from request import new_request
import requests
import json
import timeit


class MakeApiCall:
    request_hit = {}
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


