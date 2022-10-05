from geolocator_file import geo_locator
import json

class obj:
    @staticmethod
    def sort_locations(current_locations,form_data):
        foreign_locations = []
        home_locations = []
        final_list = []
        home_country = geo_locator.get_home_country_name(form_data.get('channel_id'))
        for city in current_locations:
            if geo_locator.is_foreign_country(home_country=home_country, place_name=city.get('key')):
                foreign_locations.append(city)
            else:
                home_locations.append(city)
        foreign_locations.sort(key=lambda x: x['doc_count'], reverse=True)
        home_locations.sort(key=lambda x: x['doc_count'], reverse=True)
        for item in home_locations:
            final_list.append(item)
        for item in foreign_locations:
            final_list.append(item)

        return final_list

object_1 = obj()
response = {'ctc': [{'key': '*-100000', 'doc_count': 38}, {'key': '100000-150000', 'doc_count': 23}, {'key': '150000-200000', 'doc_count': 55}, {'key': '200000-300000', 'doc_count': 77}, {'key': '300000-400000', 'doc_count': 90}, {'key': '400000-500000', 'doc_count': 50}, {'key': '500000-750000', 'doc_count': 62}, {'key': '750000-1000000', 'doc_count': 30}, {'key': '1000000-1500000', 'doc_count': 34}, {'key': '1500000-*', 'doc_count': 169}], 'preferred_locations': [{'key': 'Canada', 'doc_count': 102}, {'key': 'Chennai', 'doc_count': 61}, {'key': 'Bengaluru / Bangalore', 'doc_count': 59}, {'key': 'Delhi', 'doc_count': 57}, {'key': 'Australia', 'doc_count': 44}, {'key': 'Anywhere', 'doc_count': 39}, {'key': 'India', 'doc_count': 34}, {'key': 'Hyderabad / Secunderabad, Telangana', 'doc_count': 34}, {'key': 'Ireland', 'doc_count': 28}, {'key': 'Singapore', 'doc_count': 25}], 'preferred_functions': [{'key': 'Human Resources', 'doc_count': 215}, {'key': 'Admin/Secretarial/Front Office', 'doc_count': 179}, {'key': 'Others', 'doc_count': 168}, {'key': 'Customer Service/Call Centre/BPO', 'doc_count': 163}, {'key': 'Education/Teaching', 'doc_count': 144}, {'key': 'Health Care', 'doc_count': 145}, {'key': 'Banking, Insurance & Financial Services', 'doc_count': 113}, {'key': 'IT', 'doc_count': 84}, {'key': 'Sales/Business Development', 'doc_count': 81}, {'key': 'Hotels/restaurants', 'doc_count': 77}], 'preferred_industry': [{'key': 'NGO/Social Services', 'doc_count': 289}, {'key': 'Customer Service', 'doc_count': 123}, {'key': 'Education', 'doc_count': 121}, {'key': 'Banking/Accounting/Financial Services', 'doc_count': 113}, {'key': 'IT/Computers - Software', 'doc_count': 78}, {'key': 'Hospitals/Healthcare/Diagnostics', 'doc_count': 75}, {'key': 'Agriculture/Dairy/Forestry/Fishing', 'doc_count': 67}, {'key': 'Other', 'doc_count': 61}, {'key': 'Food & Packaged Food', 'doc_count': 61}, {'key': 'Advertising/PR/Events', 'doc_count': 55}], 'count': 1279, 'experience': [{'key': '*-1.0', 'doc_count': 74}, {'key': '1.0-3.0', 'doc_count': 223}, {'key': '3.0-5.0', 'doc_count': 139}, {'key': '5.0-7.0', 'doc_count': 106}, {'key': '7.0-10.0', 'doc_count': 108}, {'key': '10.0-15.0', 'doc_count': 87}, {'key': '15.0-*', 'doc_count': 59}], 'preferred_roles': [{'key': {'function': 'Admin/Clerical/Secretarial', 'roles': 'Administration Executive'}, 'doc_count': 2}, {'key': {'function': 'Admin/Clerical/Secretarial', 'roles': 'Computer Operator/Stenographer/Data Entry'}, 'doc_count': 2}, {'key': {'function': 'Admin/Clerical/Secretarial', 'roles': 'Executive Secretary/Personal Assistant'}, 'doc_count': 1}, {'key': {'function': 'Admin/Clerical/Secretarial', 'roles': 'Marketing Manager'}, 'doc_count': 1}, {'key': {'function': 'Admin/Clerical/Secretarial', 'roles': 'Typist'}, 'doc_count': 1}, {'key': {'function': 'Admin/Clerical/Secretarial', 'roles': 'VP/GM/Head - Sales'}, 'doc_count': 1}, {'key': {'function': 'Admin/Secretarial/Front Office', 'roles': 'AR Caller/AR Analyst'}, 'doc_count': 1}, {'key': {'function': 'Admin/Secretarial/Front Office', 'roles': 'Accessory Designer'}, 'doc_count': 1}, {'key': {'function': 'Admin/Secretarial/Front Office', 'roles': 'Account Manager - Direct Marketing'}, 'doc_count': 1}, {'key': {'function': 'Admin/Secretarial/Front Office', 'roles': 'Account Mgr/Mgr - Client Servicing (PR)'}, 'doc_count': 1}], 'current_location': [{'key': 'Philippines', 'doc_count': 87}, {'key': 'Delhi', 'doc_count': 71}, {'key': 'Chennai', 'doc_count': 61}, {'key': 'India', 'doc_count': 50}, {'key': 'Bengaluru / Bangalore', 'doc_count': 43}, {'key': 'Nagpur', 'doc_count': 24}, {'key': 'Egypt', 'doc_count': 19}, {'key': 'Hyderabad / Secunderabad, Telangana', 'doc_count': 20}, {'key': 'Kolkata', 'doc_count': 18}, {'key': 'Mumbai', 'doc_count': 16}], 'covid_layoffed': [{'key': 0, 'doc_count': 710}, {'key': 1, 'doc_count': 289}]}
form_data = {'express_resumes': {'size': 1, 'from': 0}, 'size': 20, 'recruiter_db_access_contexts': ['rexmonster'], 'from': 0, 'sub_channel_id': 1, 'recruiter_company_name': 'Monster Test', 'subuid': 792916, 'channel_id': 1, 'corp_id': 523830, 'site_context': 'rexmonster', 'filters': {'company': {'currency': 'INR', 'include_profiles_with_no_notice_period': 1}, 'additional': {'show_active_created': 'active', 'active_created_days': 180}, 'education': {'highest_second_cond': 'AND', 'yop_from': 0, 'yop_to': 0, 'highest': [{'degree': 'Bachelor of Social Work (B.S.W)', 'specializations': ['Social Work'], 'condition': 'OR'}]}}, 'strict': True, 'refine_search': {'sort_by': 'relevance'}, 'queries': {'search_scope_id': 1}}
response['current_location'] = obj.sort_locations(current_locations=response.get("current_location"), form_data=form_data)

print(json.dumps(response,indent=4))