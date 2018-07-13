# Common Application to test the data
# ---------------------------------------------

from requests import get
from requests import post
import json
from datetime import datetime

config = None
with open("../config.json", 'r+') as f:
    config = json.load(f)
EAPI_PORT = config["ElasticAPI"]["port"]
MAPPER_PORT = config["EAPIMapper"]["port"]
HOST = config["Common"]["host"]

def getLogsById(logId):
    print(get("http://" + HOST + ":" + str(EAPI_PORT) + "/logs/" + str(logId)).json())

def getAllLogs(limit):
    print(get("http://" + HOST + ":" + str(EAPI_PORT) + "/logs/getall/" + str(limit)).json())

def getLogsBetweenDateFrame():
    startDate = "2018/07/10"
    endDate = "2018/07/15"
    startTimeStamp = datetime.strptime(startDate, "%Y/%m/%d")
    startTimeStamp = startTimeStamp.strftime("%Y%m%d000000")
    endTimeStamp = datetime.strptime(endDate, "%Y/%m/%d")
    endTimeStamp = endTimeStamp.strftime("%Y%m%d000000")
    print(get("http://" + HOST + ":" + str(EAPI_PORT) + "/logs/date/"+startTimeStamp+"/"+ endTimeStamp).json())

getLogsById(20180709120505)
getAllLogs(10)
getLogsBetweenDateFrame()

