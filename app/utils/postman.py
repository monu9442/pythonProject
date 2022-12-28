from app.utils.constants import request_body
import requests


class Postman:

    def __init__(self, API_PATH):
        self.api = API_PATH

    def hit_post_request(self, api_path, request_body):
        result = requests.post(api_path, json= request_body)
        if result:
            json_result = result.json()
        return json_result

    def hit_get_request(self, api_path, request_body):
        result = requests.get(api_path, json= request_body)
        if result:
            json_result = result.json()
        return json_result
