import pymongo
import json

client = pymongo.MongoClient('localhost:27017')

collection = client['books']['book_details']

query_filter1 = {'author': 'Unknown'}
query_filter2 = {'pages':{'$lte':200}}
query_filter3 = {}

for doc_searched in collection.find({'author':'Chinua Achebe','pages':{'$lte' : 300}]):
    print(collection)
    print(doc_searched)