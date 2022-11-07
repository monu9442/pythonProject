import requests
from app.utils.profile_data import request_body, ES_QUERY
import json
from time import time
from elasticsearch import Elasticsearch

def get_elastic_result(ES_CONN, es_query):
    result = ES_CONN.search(es_query)
    return result

def create_profile_dicts():
    profile_dicts = []
    size = 100
    try:
        ES_CONNECTOR = Elasticsearch(["http://172.30.28.46:9200", "http://172.30.28.47:9200"], maxsize=25, timeout=120,
                                 http_auth=('readonly', 'readonly'))
    except Exception as E:
        print(f"Exception : {E}")
    count = 1
    while len(profile_dicts) < 100:
        # print(f"Request {count} fired to elastic.....")
        es_results = ES_CONNECTOR.search(body= ES_QUERY, index='livecore_india')
        count += 1
        for result in es_results['hits']['hits']:
            temp = dict()
            profile = result['_source']
            id = profile.get("profile_id", None)
            skills = profile.get("skills", None)
            designation = profile.get("current_employment").get("designation", None)
            employer = profile.get("current_employment").get("employer", None)
            if id and skills and designation and employer and len(skills) > 2:
                temp["id"] = id
                temp["skills"] = skills
                temp["designation"] = designation
                temp["company"] = employer
                profile_dicts.append(temp)
        ES_QUERY['from'] += size
    return profile_dicts

def get_n_words(entity_list, n):
    if len(entity_list) <= n or n == -1:
        return entity_list
    else:
        entity_list_new = []
        for i in range(0,n):
            entity_list_new.append(entity_list.pop(0))
        return entity_list_new

def modify_request(profile, hit_request_body, number_of_words):
    hit_request_body['profile_id'] = profile.get("id")
    hit_request_body['profile_skills'] = get_n_words(profile.get("skills"), number_of_words)
    hit_request_body['profile_designation'] = profile.get("designation")
    hit_request_body['profile_company'] = profile.get("company")
    return hit_request_body

def hit_request(api, request):
    result = requests.post(api, json=request)
    result = result.json()
    return result

def main(n, profile_dicts):
    api = "http://rec-dev-nm.monsterindia.com/polaris/similar_profiles"

    Total_skill_count = 0
    start = time()
    for profile in profile_dicts:
        try:
            Total_skill_count += len(profile.get("skills"))
            req = modify_request(profile, request_body, n)
            result = hit_request(api, req)
        except Exception as e:
            print(f"Error:{e}")
    end = time()
    if n ==-1:
        print(f"Total number of Skills = {Total_skill_count} and Avg Skills = {Total_skill_count/len(profile_dicts)}")
    print(f"Time taken for {n} Words for 100 profiles = {end-start} and avg_time = {(end-start)/len(profile_dicts)}")


profile_dicts = create_profile_dicts()
main(-1, profile_dicts)
main(10, profile_dicts)
main(5, profile_dicts)


