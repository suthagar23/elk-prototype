# Common Application to test the data
# ---------------------------------------------

from requests import post
import json

config = None
with open("../config.json", 'r+') as f:
    config = json.load(f)
EAPI_PORT = config["ElasticAPI"]["port"]
MAPPER_PORT = config["EAPIMapper"]["port"]
HOST = config["Common"]["host"]

def insertNginxLogsToElasticAPI():
    with open("../sampleLogs/nginx_logs.txt", "r") as data_file:
        data = data_file.readlines()
        for entry in data:
            print(post("http://" + HOST + ":" + str(MAPPER_PORT) + "/mapper/nginx/logs", json=entry).json())

insertNginxLogsToElasticAPI()