import json
import os

with open(os.getcwd()+"/app/menu.json",'r+') as read_file:
    data = json.load(read_file)

with open(os.getcwd()+"/app/user.json",'r+') as read_user:
    users_data=json.load(read_user)
    users_db = users_data["user"]

def read_menu():
    return data

def read_user():
    return users_data