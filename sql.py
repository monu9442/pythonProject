from mysql import connector
import mysql
import json

try:
    conn = mysql.connector.connect(host='172.30.10.24', user='Akhileshn', password='@kh!le$hnwert', database="bazooka")
    print('connection successfull.................')
    query = "select distinct(current_location_text) from user_profiles up Where up.kiwi_profile_id IS NOT NULL AND (" \
            "up.deleted = 0 OR up.deleted IS NULL) AND up.enabled = 1 AND up.searchable=1 and current_location_text " \
            "is not NULL and up.site_context = '"
    country_list = ["IN","SG","AE","PH","MY","HK","TH","ID","PK","JO","FR","EG","BD","SE","QA","CA","AU","BH","OM","SA","LB","CH","CN","NZ","TW","AF","YE","DE","NL","NP","KW","BE","IE","ES","JP","MV","IQ","MX","VN","HG","UAE","US","GB","ZA","PL","BR"]
    site_context_list = ['rexmonster','monstergulf','monsterhongkong','monstersingapore','monsterphilippines','monsterthailand','monstervietnam','monsterindonesia','monstermalaysia']
    cursor = conn.cursor()
    location_data = dict()
    for site_context in site_context_list:
        print(f'Executing query for site context = {site_context}')
        distinct_city_list = []
        final_query = query + site_context + "'"
        cursor.execute(final_query)
        db_data = cursor.fetchall()
        for row in db_data:
            for data in row:
                distinct_city_list.append(data)
        print(distinct_city_list)
        location_data[site_context] = distinct_city_list

    with open('locations.txt', 'w') as convert_file:
        convert_file.write(json.dumps(location_data, indent=3))

except Exception as e:
    print('could not connect.....')
    print(f"Error = {e}")
