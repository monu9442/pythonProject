from mysql import connector
import mysql
import json
import pandas as pd


def get_insert_value(corp_id, feature_name, feature_id, enabled):
    return f"({corp_id}, {feature_id}, {feature_name}, {enabled}),"

def get_insert_query_string(db_data):
    INSERT_QUERY = "INSERT INTO recruiter_feature_access(rec_id, feature_id, feature_name, enabled) VALUES "
    insert_value_string = ""
    for data in db_data:
        insert_value_string += get_insert_value(data[0],"'full text resume'", 2, 1)
    insert_value_string = insert_value_string[:-1]
    return INSERT_QUERY + insert_value_string

def get_search_query_string(xcodes):
    SEARCH_QUERY = "SELECT id, xcode from corps where xcode in ("
    for xcode in xcodes:
        SEARCH_QUERY += f"'{xcode}',"
    SEARCH_QUERY = SEARCH_QUERY[:-1]
    SEARCH_QUERY += ")"
    return SEARCH_QUERY

def get_xcodes_already_in_db():
    x_code_list = []
    query = 'select xcode from corps where id in (select rec_id from recruiter_feature_access);'
    db_data = execute(query)
    for data in db_data:
        x_code_list.append(data[0])
    return x_code_list



def execute(query):
    try:
        conn = mysql.connector.connect(host='172.30.10.24', user='Akhileshn', password='@kh!le$hnwert',
                                       database="bazooka")
        print('connection successfull.................')
        cursor = conn.cursor()
        cursor.execute(query)
        db_data = cursor.fetchall()
        conn.close()
        return db_data
    except Exception as e:
        print({e})

def get_clear_xcodes(list_of_xcodes):
    final_list = []
    for xcode in list_of_xcodes:
        final_list.append(xcode)
    return final_list

def create_req_body(old_xcodes, new_xcodes):
    count = 0
    request_body = dict()
    for xcode in new_xcodes:
        if count >= 1000:
            break
        if xcode in old_xcodes:
            continue
        else:
            temp = {xcode: {"enable":[2]}}
            request_body.update(temp)
            count += 1
    return request_body

def main():
    try:
        x_codes_already_in_db = get_xcodes_already_in_db()
        df = pd.read_excel(r'C:\Users\anandwal\Downloads\nov_data.xlsx')
        new_xcodes = df['xcode']
        new_xcodes = get_clear_xcodes(new_xcodes)
        request_body = create_req_body(x_codes_already_in_db, new_xcodes)
        print(json.dumps(request_body, indent=3))


    except Exception as E:
        print(E)


main()
