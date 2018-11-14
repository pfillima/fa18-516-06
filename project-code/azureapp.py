import pyodbc
from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class AzureSQLAdmin(Resource):
    def get(self):
        server = 'pfillimansql.database.windows.net'
        database = 'AdvWorksLT'
        username = 'sqladmin'
        password = 'SqlDba123'
        driver= '{ODBC Driver 13 for SQL Server}'
        connexion = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = connexion.cursor()
        cursor.execute("select * from sys.tables")
        row = cursor.fetchone()
        while row:
           GeneratedCode = str(row[0])
           ReportedDate = str(row[1])
           print (str(row[0]) + " " + str(row[1]))
           row = cursor.fetchone()

        rest_row = jsonify(row)
        return rest_row

api.add_resource(AzureSQLAdmin, '/')

if __name__ == '__main__':
    app.run()
    
