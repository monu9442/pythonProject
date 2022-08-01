import json

class Data_sender:
    def send_data(self):
        json_file = open('json_data.txt')
        documents = json.load(json_file)
        return documents
