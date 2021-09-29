import json


def save_data(data):
    file = open('./save/data.txt',mode='w')
    json.dump(data,file)