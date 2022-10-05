# import time
# import pandas as pd
# from geolocator_file import geo_locator
#
# df = pd.read_csv("list_of_cities.csv")
# cities = df['Name of City']
# country_list = []
# exception_cities = []
# start = time.time()
# for city in cities:
#     try:
#         if geo_locator.is_foreign_country("India", city):
#             country_list.append("True")
#         else:
#             country_list.append('False')
#     except:
#         exception_cities.append(city)
#         continue
#
# end = time.time()
# print(f"Time taken to process = {end - start}")
# print(exception_cities)

# your code goes here
from datetime import datetime, timedelta
today = datetime.today()
old_date = today - timedelta(3 * 30)
timestamp = int(datetime.timestamp(old_date) * 1000)
sql_query = ""
sql_query += f" AND uad.active_at > {timestamp}"
print(sql_query)
