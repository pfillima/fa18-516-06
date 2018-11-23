#!flask/bin/python
import pyodbc
import requests
import json
import config
import datetime
import urllib.request
import mongoengine
import models
import pymongo
from flask import Flask, request, jsonify
from flask_restful import fields
from bson import json_util

app = Flask(__name__)


##################################################
server = 'pfillimansql.database.windows.net'
database = 'AdvWorksLT'
username = 'sqladmin@pfillimansql'
password = 'XXXX'
driver = '{ODBC Driver 13 for SQL Server}'
mongouid = 'mongoadmin'
mongopwd = 'XXX'
##################################################


def buildOpenWeatherMapAPIRequest(apikey, cityname):
    return "http://api.openweathermap.org/data/2.5/weather?q=" + cityname + "&appid=" + apikey


def convertTime(tm):
    # convert time into SQL datetime format
    return datetime.datetime.fromtimestamp(int(tm)).strftime("%Y-%m-%d %H:%M:%S")

def convertTemperature(temp):
    # convert degrees Kelvin to degrees Fahrenheit
    return ((temp - 273.15) * (9.0 / 5.0)) + 32


def getAPIData(url):
    con = urllib.request.urlopen(url)
    data = con.read().decode("utf-8")
    weatherjson = json.loads(data)
    con.close()

    return weatherjson


def createSQLTable(connstr):
    conn = pyodbc.connect(connstr)
    sql_createtable = \
            "IF NOT EXISTS ( SELECT 1 FROM sys.tables WHERE OBJECT_ID = OBJECT_ID('dbo.OpenWeatherAPI')) " \
            "CREATE TABLE dbo.OpenWeatherAPI ( " \
                 "ID int identity(1,1) primary key, " \
                 "Time datetime2(7), " \
                 "Location varchar(50), " \
                 "Condition varchar(20), " \
                 "ConditionDescription varchar(50), " \
                 "Temperature numeric(10,5), " \
                 "Pressure numeric(10,5), " \
                 "Humidity numeric(10,5), " \
                 "WindSpeed numeric(10,5), " \
                 "WindDegrees numeric(10,5), " \
                 "CreatedDate datetime not null default(getdate()))"

    cursor = conn.cursor()
    cursor.execute(sql_createtable)
    cursor.commit()
    cursor.close()


def parseData(jsondata):
    # create dictionary to hold current parsed result
    result = {}

    # parse the json into variables
    result["Time"] = jsondata.get("dt")
    result["Temperature"] = jsondata.get("main").get("temp")
    result["Location"] = jsondata.get("name")
    result["Humidity"] = jsondata.get("main").get("humidity")
    result["Pressure"] = jsondata.get("main").get("pressure")
    result["Condition"] = jsondata["weather"][0]["main"]
    result["ConditionDesc"] = jsondata["weather"][0]["description"]
    result["WindSpeed"] = jsondata.get("wind").get("speed")
    result["WindDeg"] = jsondata.get("wind").get("deg")

    return result


def insertAzureTable(connstr, jsondata):
    # parse the json into variables
    dict = parseData(jsondata)

    Time = convertTime(dict["Time"])
    Temperature = convertTemperature(dict["Temperature"])
    Location = dict["Location"]
    Condition = dict["Condition"]
    ConditionDesc = dict["ConditionDesc"]
    Pressure = dict["Pressure"]
    Humidity = dict["Humidity"]
    WindSpeed = dict["WindSpeed"]
    WindDeg = dict["WindDeg"]

    # Create the Azure SQL table, if it does not exist
    createSQLTable(connstr)

    # insert into table
    conn = pyodbc.connect(connstr)

    sqlinsert = "INSERT INTO dbo.OpenWeatherAPI (Time, Location, Condition, ConditionDescription, Temperature, Pressure, Humidity, WindSpeed, WindDegrees) " \
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    values = [Time, Location, Condition, ConditionDesc, Temperature, Pressure, Humidity, WindSpeed, WindDeg]

    cursor = conn.cursor()
    cursor.execute(sqlinsert, values)
    cursor.commit()
    cursor.close()


def insertMongoDB(jsondata):
    connstr = "mongodb://"+mongouid+":"+mongopwd+"@pfmongodbcluster0-shard-00-00-16fyb.mongodb.net:27017, " \
              "pfmongodbcluster0-shard-00-01-16fyb.mongodb.net:27017," \
              "pfmongodbcluster0-shard-00-02-16fyb.mongodb.net:27017/" \
              "test?ssl=true&replicaSet=PFMongoDBCluster0-shard-0&authSource=admin&retryWrites=true"

    # create the connection to MongoDB and insert the json weather data
    conn = pymongo.MongoClient(connstr)

    db = conn.WeatherDB
    weathercol = db.WeatherCollection

    weatherclean = json.loads(json_util.dumps(jsondata))
    weathercol.insert_one(weatherclean)

    conn.close()


@app.route("/weather", methods=["GET"])
def get_weather():
    # grab weather info from openweatherapi
    openweatherkey = "338f5c207f400c983df8f00e1ce658ac"
    city = "Indianapolis,US"
    url = buildOpenWeatherMapAPIRequest(openweatherkey, city)
    jsondata = getAPIData(url)

    # get dbname from api parameter
    dbname = request.args.get('dbname')

    if (dbname == 'azuresql'):
        connstr = 'DRIVER={driver};PORT=1433;SERVER={server};DATABASE={database};UID={username};PWD={password}'.format(driver=driver,server=server,database=database,username=username,password=password)
        insertAzureTable(connstr, jsondata)

    elif (dbname == 'mongodb'):
        insertMongoDB(jsondata)

    else:
        print("Please use 'azuresql' or 'mongodb'")

    return jsonify(jsondata)


if __name__ == '__main__':
    app.run()


