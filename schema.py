from graphene import ObjectType, String, Boolean, ID, List, Field, Int
import json
import os
import requests
from collections import namedtuple


def _json_object_hook(d):
    return namedtuple('X', d.keys())(*d.values())

def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)


class user(ObjectType):
    name = String()
    id = ID()
    email = String()


class post(ObjectType):
    id = ID()
    title = String()
    user = Field(user)


class Query(ObjectType):
    users = List(user, id=Int(required=True))
    def resolve_users(self, info, id):
        response = requests.get('https://jsonplaceholder.typicode.com/users')
        return json2obj(json.dumps(response.json()))
    
    user = Field(user, id=Int(required=True))
    def resolve_user(self, info, id):
        response = requests.get('https://jsonplaceholder.typicode.com/users')
        response = response.json()
        output = {}
        for item in response:
            if item["id"] == id:
                output = item
                break
        return json2obj(json.dumps(output))

    post = Field(post, id=Int(required=True))
    def resolve_post(self, info, id):
        response = requests.get('https://jsonplaceholder.typicode.com/posts')
        response = response.json()
        output = {}
        for item in response:
            if item["id"] == id:
                output = item
                break
        return json2obj(json.dumps(output))