import json

with open('data/userList.json', encoding="utf8") as f:
    json_object = json.load(f)

print(json_object)
