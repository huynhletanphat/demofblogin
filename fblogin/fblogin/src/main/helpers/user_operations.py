import json

def load_users(users_file):
    with open(users_file, "r") as f:
        return json.load(f)