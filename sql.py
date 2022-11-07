from mysql import connector
import mysql
import json

def convert_data_into_dictionary(data):
    temp = dict()
    for row in data:
        printrow['id']
        temp.update({row[0]: row[1]})
    return temp

try:
    conn = mysql.connector.connect(host='172.30.10.10', user='Akhileshn', password='@kh!le$hnwert', database="falcon")
    print('connection successfull.................')
    query = "SELECT id, resume_file_path from user_profiles  WHERE id in (4, 10, 12, 15, 16, 78)"
    cursor = conn.cursor()
    cursor.execute(query)

    db_data = cursor.fetchall()
    db_data = convert_data_into_dictionary(db_data)

    if 4 in db_data:
        print("true")
        if db_data[4].startswith()
        print(db_data[4])


except Exception as e:
    print({e})
