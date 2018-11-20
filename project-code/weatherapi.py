#!flask/bin/python
import pyodbc
import requests
import json
import config
import datetime
import urllib.request
from flask import Flask, request, jsonify
from flask_restful import fields

app = Flask(__name__)


##################################################
server = 'pfillimansql.database.windows.net'
database = 'AdvWorksLT'
username = 'sqladmin@pfillimansql'
password = 'XXXXXXXXX'
driver = '{ODBC Driver 13 for SQL Server}'
##################################################


def buildOpenWeatherMapAPIRequest(apikey, cityname):
    return "http://api.openweathermap.org/data/2.5/weather?q=" + cityname + "&appid=" + apikey


def getAPIData(url):
    con = urllib.request.urlopen(url)
    data = con.read().decode("utf-8")
    weatherjson = json.loads(data)
    con.close()

    return weatherjson


def createSQLTable(connstr):
    conn = pyodbc.connect(connstr)

    sql_createtable = "IF NOT EXISTS ( SELECT 1 FROM sys.tables WHERE OBJECT_ID = OBJECT_ID('dbo.OpenWeatherAPI')) " \
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


def insertWeatherToAzureTable(connstr, jsondata):
    # parse the json into variables
    Time = jsondata.get("dt")
    Location = jsondata.get("name")
    Temperature = jsondata.get("main").get("temp")
    Humidity = jsondata.get("main").get("humidity")
    Pressure = jsondata.get("main").get("pressure")
    Condition = jsondata["weather"][0]["main"]
    ConditionDesc = jsondata["weather"][0]["description"]
    WindSpeed = jsondata.get("wind").get("speed")
    WindDeg = jsondata.get("wind").get("deg")

    # convert time into SQL datetime format
    Time = datetime.datetime.fromtimestamp(int(Time)).strftime("%Y-%m-%d %H:%M:%S")

    # convert degrees Kelvin to degrees Fahrenheir
    Temperature = ((Temperature - 273.15) * (9.0 / 5.0)) + 32


    conn = pyodbc.connect(connstr)

    # insert into table
    sqlinsert = "INSERT INTO dbo.OpenWeatherAPI (Time, Location, Condition, ConditionDescription, Temperature, Pressure, Humidity, WindSpeed, WindDegrees) " \
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    values = [Time, Location, Condition, ConditionDesc, Temperature, Pressure, Humidity, WindSpeed, WindDeg]

    cursor = conn.cursor()
    cursor.execute(sqlinsert, values)
    cursor.commit()
    cursor.close()


@app.route("/", methods=["GET"])
def get_apiweather():

    try:
        connstr = 'DRIVER={driver};PORT=1433;SERVER={server};DATABASE={database};UID={username};PWD={password}'.format(driver=driver,server=server,database=database,username=username,password=password)
        createSQLTable(connstr)

        openweatherkey = "338f5c207f400c983df8f00e1ce658ac"
        city = "Indianapolis,US"
        url = buildOpenWeatherMapAPIRequest(openweatherkey, city)
        jsondata = getAPIData(url)

        # parse and insert into Azure SQL persistent storage
        insertWeatherToAzureTable(connstr, jsondata)

        return jsonify(jsondata)

    except:
        return "ERR"


if __name__ == '__main__':
    app.run()


