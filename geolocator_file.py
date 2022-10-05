from geopy.geocoders import Nominatim


class Geopy:

    def is_foreign_city(self, home_country, place_name):
        geolocator = Nominatim(user_agent="Polaris")
        location = geolocator.geocode(place_name)
        coordinates = f"{location.latitude},{location.longitude}"
        address = geolocator.reverse(coordinates).raw['address']
        country_name = address.get('country', "")

        if country_name.lower() in home_country:
            return False
        else:
            return True

    def get_home_country_name(self, site_context):
        if site_context == 'rexmonster':
            return ["india"]
        elif site_context == 'monstergulf':
            return ["united arab emirates", "saudi arabia", "bahrain",
                    "iran", "iraq", "kuwait", "oman", "qatar", "yemen"]
        elif site_context == 'monsterhongkong':
            return ["hong Kong", "hongkong"]
        elif site_context == 'monstersingapore':
            return ["singapore"]
        elif site_context == 'monsterphilippines':
            return ["philippines"]
        elif site_context == 'monsterthailand':
            return ['thailand']
        elif site_context == 'monstervietnam':
            return ['vietnam']
        elif site_context == 'monsterindonesia':
            return ['indonesia']
        elif site_context == 'monstermalaysia':
            return ['malaysia']

    def get_country_name(self, list_of_countries):
        geolocator = Nominatim(user_agent="Polaris")
        country_list = []
        for place in list_of_countries:
            location = geolocator.geocode(place)
            coordinates = f"{location.latitude},{location.longitude}"
            address = geolocator.reverse(coordinates).raw['address']
            country_name = address.get('country', "")
            country_list.append(country_name)
        return country_list

geo_locator = Geopy()
