import json
from time import time
from geopy.geocoders import Nominatim
from geolocator_file import geo_locator
try:
    file = open('site_context_location_list.json')
    loaded_dict = json.load(file)
    filtered_data = dict()
    site_contexts = ['monstergulf', 'monsterhongkong', 'monstersingapore', 'monsterphilippines', 'monsterthailand', 'monstervietnam', 'monsterindonesia', 'monstermalaysia']
    for site_context in site_contexts:
        home_country = geo_locator.get_home_country_name(site_context)
        home_country_in_regional = geo_locator.get_country_name(home_country)
        home_country += home_country_in_regional
        home_cities = []
        foriegn_cities = []
        city_list = loaded_dict[site_context]
        for city in city_list:
            try:
                if not geo_locator.is_foreign_city(home_country, city):
                    home_cities.append(city)
                else:
                    foriegn_cities.append(city)
            except:
                foriegn_cities.append(city)
        filtered_data[site_context] = home_cities

    file = open('filtered_data.txt', 'w')
    file.write(json.dumps(filtered_data, indent=3))


except Exception as e:
    print(f"Error : {e}")

