def get_mongo_formatted_data(similar_profile_list):
    formatted_list_of_profiles = []
    for profile in similar_profile_list:
        temp = dict()
        temp['source_profile_id'] = profile
        temp['industry'] = similar_profile_list[profile]['industry']
        temp['similar_profile_count'] = similar_profile_list[profile]['similar_profile_count']
        temp['similar_profiles'] = similar_profile_list[profile]['similar_profiles']

        formatted_list_of_profiles.append(temp)

    return formatted_list_of_profiles


data = {10004: {'industry': None, 'similar_profile_count': 10, 'similar_profiles': ['8927308', '1771951', '12972588', '5496531', '91038336', '56374987', '34782201', '43048237', '49442142', '16449919']}, 10005: {'industry': None, 'similar_profile_count': 10, 'similar_profiles': ['55342497', '9270627', '39947341', '37610775', '9913979', '44662681', '22333194', '10671189', '12376030', '36478759']}, 10006: {'industry': None, 'similar_profile_count': 10, 'similar_profiles': ['12574446', '28300578', '29470401', '9452573', '25764059', '6004674', '86347017', '20418799', '44587935', '12260335']}, 10010: {'industry': None, 'similar_profile_count': 10, 'similar_profiles': ['4106898', '664756', '982641', '93861009', '22149891', '45066929', '3301255', '29036803', '13870072', '1804776']}, 10001: {'industry': None, 'similar_profile_count': 0, 'similar_profiles': []}, 10002: {'industry': None, 'similar_profile_count': 10, 'similar_profiles': ['41196639', '90452203', '97027286', '92832535', '87866479', '57510934', '92860850', '30071818', '49596792', '27641432']}}

format_list = get_mongo_formatted_data(data)
for data in format_list:
    print(data)