

from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from datetime import datetime
from flask_cors import CORS
import inspect
import json

app = Flask(__name__)
CORS(app)
config = None
with open("config.json", 'r+') as f:
    config = json.load(f)
LOG_ENABLED = config["ElasticAPI"]["logEnabled"]
PORT = config["ElasticAPI"]["port"]
DEBUG_MODE = config["ElasticAPI"]["debug"]
MONGODB_HOST = config["Common"]["mongoDBHost"]
MONGODB_NAME = config["Common"]["mongoDBName"]
mongo = PyMongo(app, MONGODB_HOST + "/" + MONGODB_NAME)

@app.route("/logs", methods=["POST"])
def saveLogs():
    data = request.get_json()
    if not data:
        data = {"response": "ERROR"}
        return jsonify(data)
    else:
        data = insertSystemDateIndexToData(data)
        printInfoLogs(data)

        mongo.db.tweets.update(
            {"_id": int(data.get('id'))},
             {"$set": {"body": data}},
            w=1, upsert=True)
        return jsonify({"response": "Saved", "id": data.get('id')})

@app.route("/logs/<string:id>", methods=["GET"])
def getLogsById(id):
    if id:
        data = mongo.db.tweets.find_one_or_404({"_id": id})
        data = removeSystemDataIndexFromData(data)
        return jsonify({"response" : id, "data" : data['body']})
    else:
        return jsonify({"response": "ERROR", "message" : "log id is missing"})

@app.route("/logs/getall/", methods=["GET"])
@app.route("/logs/getall/<string:limit>", methods=["GET"])
def getAllLogs(limit=None):
    if limit:
        if int(limit)>0:
            collection = mongo.db['tweets']
            cursor = collection.find().sort([('$natural',-1)]).limit(int(limit))
            data = []
            for document in cursor:
                data.append(removeSystemDataIndexFromData(document)['body'])
            return jsonify({"response" :  "Get all logs (limit : " + limit + ")", "data" : data})
        else:
            return jsonify({"response": "ERROR", "message": "incorrect log request limit"})
    else:
        return jsonify({"response": "ERROR", "message" : "log request limit is missing"})

@app.route("/logs/date/", methods=["GET"])
@app.route("/logs/date/<string:startTimeStamp>", methods=["GET"])
@app.route("/logs/date/<string:startTimeStamp>/<string:endTimeStamp>", methods=["GET"])
def getLogsByDateFrame(startTimeStamp=None, endTimeStamp=None):
    if (startTimeStamp or endTimeStamp):
        query = None
        if startTimeStamp:
            query = {"_id":{"$gt": int(startTimeStamp)}}
        if endTimeStamp:
            query = {"_id": {"$gt": int(startTimeStamp), "$lt": int(endTimeStamp)}}

        print(str(query))
        collection = mongo.db['tweets']
        cursor = collection.find(query).sort([('$natural',-1)]).limit(100)
        data = graphingData(cursor)
        return jsonify(data)
    else:
        return jsonify({"response": "ERROR", "message" : "Datetime stamp is missing"})

def graphingData(collections):
    data = []
    dateTimeVsCount = {}
    for document in collections:
        dataBody = removeSystemDataIndexFromData(document)['body']
        data.append(dataBody)

        dateTime = dataBody["dateTime"].split(":")[0]
        if dateTime in dateTimeVsCount:
            dateTimeVsCount[dateTime] += 1
        else:
            dateTimeVsCount[dateTime] = 1

    labels = []
    values = []
    for item in sorted(list(dateTimeVsCount.keys())):
        labels.append(item)
        values.append(dateTimeVsCount[item])

    dateTimeVsCountRespones = {
        "labels" : labels,
        "values" : values,
        "date" : dateTimeVsCount
    }
    return {"response" :  "Get all logs (limit : 100)", "data" : data, "dateTimeVsCount" : dateTimeVsCountRespones}

@app.errorhandler(404)
def new_page(error):
    return jsonify({"response": "ERROR", "message": "404 Not Found"})

def insertSystemDateIndexToData(data) :
    timeNow = datetime.now()
    data['system_timestamp'] = str(timeNow)
    logDateTime = data["dateTime"].split(" ")[0]
    logDateTimeStamp = datetime.strptime(logDateTime, "%d/%m/%Y:%H:%M:%S")
    logDateTimeStamp=logDateTimeStamp.strftime('%Y%m%d%H%M%S')
    data['id'] = str(logDateTimeStamp)
    return data

def removeSystemDataIndexFromData(data):
    if "system_timestamp" in data['body']:
        del data['body']['system_timestamp']
    return  data

def printInfoLogs(logLine):
    if(LOG_ENABLED):
        print("INFO [" + str(datetime.now()) + "] ElasticApi." + inspect.stack()[1][3] + " - " + str(logLine));

if __name__ == "__main__":
    app.run(debug=DEBUG_MODE,port=PORT)