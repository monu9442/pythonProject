from mysql import connector
import mysql
import json
import pandas as pd
from elasticsearch.client import Elasticsearch
from app.utils.queue import RabbitMqConnector

main_query = {
  "size":2000,
  "_source": ["profile_id"],
  "query": {
    "terms": {
      "kiwi_user_id": [
      ]
    }
  }
}

msg = {"id":"null", "index":"yang", "type":"profile"}

def get_es_results(kiwi_user_ids):
    try:
        main_query['query']['terms']['kiwi_user_id'] = kiwi_user_ids
        ES_CONN = Elasticsearch('http://172.30.28.47:9200', maxsize=25, timeout=120, http_auth=('readonly', 'readonly'))
        results = ES_CONN.search(body=main_query, index='livecore_india')
        return results
    except Exception as e:
        print(f"Cannot fetch results : {e}")

def execute(query):
    try:
        conn = mysql.connector.connect(host='10.216.247.68', user='appuser', password='dbpassword',database="falcon")
        print('connection successfull to DB2')
        cursor = conn.cursor()
        cursor.execute(query)
        db_data = cursor.fetchall()
        conn.close()
        return db_data
    except Exception as e:
        print({e})

def extract_kiwi_profile_ids(db_data):
    id_list = []
    for data in db_data:
        id_list.append(data[0])
    return id_list

def extract_profile_ids(es_results):
    id_list = []
    for es_result in es_results['hits']['hits']:
        id = es_result['_source'].get('profile_id')
        msg['id'] = id
        RabbitMqConnector.publish_data(msg)
    return id_list

def get_profile_ids(offset):
    sql_query = f'select uid as kiwi_profile_id from seeker_brandings  where uid is not NULL ORDER BY uid LIMIT {offset}, 2000;'
    db_data = execute(sql_query)
    kiwi_user_ids = extract_kiwi_profile_ids(db_data)
    es_results = get_es_results(kiwi_user_ids)
    profile_ids = extract_profile_ids(es_results)

    return profile_ids

def main():
    query = "SELECT id as id, kiwi_profile_id as res_id from user_profiles WHERE kiwi_profile_id = 73451518"
    db_data = execute(query)
    for data in db_data:
        print(data)

main()
