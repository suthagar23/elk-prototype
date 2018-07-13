from flask import Flask, request, jsonify
from datetime import datetime
import inspect
import re
from requests import post
import json

app = Flask(__name__)

config = None
with open("config.json", 'r+') as f:
    config = json.load(f)
LOG_ENABLED = config["EAPIMapper"]["logEnabled"]
PORT = config["EAPIMapper"]["port"]
DEBUG_MODE = config["EAPIMapper"]["debug"]

@app.route("/mapper/nginx/logs", methods=["POST"])
def receiveLogLines():
    data = request.get_json()
    processedData = json.loads(createJSONForElasticAPI(data))
    if(len(processedData.keys())>0) :
        printInfoLogs("Mapped the request data successfully")
        response = post("http://127.0.0.1:5001/logs", json=processedData).json()
        return jsonify(response)
    else :
        printErrorLogs("Error while mapping the data")
        return jsonify({"response": "Error while mapping the data", "logLine" : data})

def createJSONForElasticAPI(logLine):

    re1 = '((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))(?![\\d])'  # IPv4 IP Address 1
    re2 = '.*?\\['  # Non-greedy match on filler
    re3 = '(.*?)'  # Square Braces 1
    re4 = '\\].*?'  # Non-greedy match on filler
    re5 = '((?:[a-z][a-z]+))'  # Word 1
    re6 = '.*?'  # Non-greedy match on filler
    re7 = '((?:\\/[\\w\\.\\-]+)+)'  # Unix Path 1
    re8 = '.*?'  # Non-greedy match on filler
    re9 = '((?:[a-z][a-z]+))'  # Word 2
    re10 = '((?:\\/[\\w\\.\\-]+)+)'  # Unix Path 2
    re11 = '.*?'  # Non-greedy match on filler
    re12 = '".*?"'  # Uninteresting: string
    re13 = '.*?'  # Non-greedy match on filler
    re14 = '(".*?")'  # Double Quote String 1
    rg = re.compile(re1 + re2 + re3 + re4 + re5 + re6 + re7 + re8 + re9 + re10 + re11 + re12 + re13 + re14,
                    re.IGNORECASE | re.DOTALL)
    m = rg.search(logLine)
    if m:
        data = {}
        data["ipAddress"] = m.group(1)
        data["dateTime"] = m.group(2)
        data["requestMethod"] = m.group(3)
        data["resourceURL"] = m.group(4)
        data["requestType"] = m.group(5)
        data["requestTypeVersion"] = m.group(6)
        printInfoLogs(data)
        return json.dumps(data)
    else:
        return {}

def printInfoLogs(logLine):
    printLogs("INFO", logLine)

def printErrorLogs(logLine):
    printLogs("ERROR", logLine)

def printLogs(type, logLine):
    if(LOG_ENABLED):
        print(type + " [" + str(datetime.now()) + "] Mapper.Nginx." + inspect.stack()[1][3] + " - " + str(logLine));
if __name__ == "__main__":
    app.run(debug=DEBUG_MODE,port=PORT)