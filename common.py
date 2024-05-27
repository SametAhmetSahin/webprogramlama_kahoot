from pymongo import MongoClient

import random, string

from bson import ObjectId

import json

#from bunnet import Document, Indexed, init_bunnet

import models as models

def get_bare_database():
    CONNSTRING = "mongodb://mongo:27017/"
    client = MongoClient(CONNSTRING)
    return client

#client = get_bare_database()
#init_bunnet(database=client.webprogramlama_kahoot, document_models=[models.Quiz, models.User])

def get_database():
    client = get_bare_database()
    return client["kahootklonu"]

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def generate_random_string(len):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(len))
    pass
