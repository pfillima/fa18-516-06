#1flask/bin/python
import pyodbc
import requests
from flask import Flask, request, jsonify
from flask_restful import fields
import json
import config

app = Flask(__name__)


##################################################
server = 'pfillimansql.database.windows.net'
database = 'AdvWorksLT'
username = 'sqladmin@pfillimansql'
password = 'SqlDba123'
driver = '{ODBC Driver 13 for SQL Server}'
##################################################


@app.route("/", methods=["POST"])
def post():
    filename = request.form["posttest.txt"]
    with open(filename, 'r') as f:
        fileContent = f.read()

    print(fileContent)

    return fileContent



@app.route("/", methods=["GET"])
def get_apiweather():

    try:
        url = "http://api.openweathermap.org/data/2.5/weather?q=Indianapolis,USA&appid=338f5c207f400c983df8f00e1ce658ac"
        r = requests.get(url)

        return jsonify(r.json())
    except:
        return False


'''
    connstr = 'DRIVER={driver};PORT=1433;SERVER={server};DATABASE={database};UID={username};PWD={password}'.format(driver=driver, server=server, database=database, username=username, password=password)
    conn = pyodbc.connect(connstr)

    #sql = "SELECT pc.Name as CategoryName FROM [SalesLT].[ProductCategory] pc WHERE pc.Name = ?"
    #params = 'Bottom Brackets'

    


    cursor = conn.cursor()
    cursor.execute(sql, params)

    row_headers = [x[0] for x in cursor.description]
    #results =  cursor.fetchall()
    json_data = []
    content = {}

    for result in cursor.fetchall():
        content = {'CategoryName': result[0]}
        json_data.append(content)
        content = {}

    return jsonify(json_data)
'''

if __name__ == '__main__':
    app.run()


