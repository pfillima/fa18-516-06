  GNU nano 2.9.3                              sqlquery.py                                         

#1flask/bin/python
import pyodbc
from flask import Flask, request, jsonify
from flask_restful import fields
import json
import config

app = Flask(__name__)


server = 'pfillimansql.database.windows.net'
database = 'AdvWorksLT'
username = 'sqladmin@pfillimansql'
password = 'XXXXXXXXX'
driver = '{ODBC Driver 13 for SQL Server}'


@app.route('/', methods=['GET'])
def index():
    connection_string = 'DRIVER={driver};PORT=1433;SERVER={server};DATABASE={database};UID={usern$
    cnxn = pyodbc.connect(connection_string)

    cursor = cnxn.cursor()
    cursor.execute("SELECT TOP 20 pc.Name as CategoryName FROM [SalesLT].[ProductCategory] pc")

    row_headers = [x[0] for x in cursor.description]
    results =  cursor.fetchall()
    json_data = []
    content = {}
    
    for result in results:
        content = {'CategoryName': result[0]}
        json_data.append(content)
        content = {}

    return jsonify(json_data)


if __name__ == '__main__':
    app.run()
