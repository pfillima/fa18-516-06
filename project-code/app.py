#! flask/bin/python

from flask import Flask, request, jsonify, abort, make_response, url_for
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_httpauth import HTTPBasicAuth
from datetime import datetime
import pyodbc
import json
import config


app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()


class AzureSQLDatabase(object):
    connection = None
    cursor = None

    def __init__(self):
        self.connection = pyodbc.connect(config.CONN_STRING)
        self.cursor = self.connection.cursor()

    def query(self, query, params):
        return self.cursor.execute(query, params)

    def commit(self):
        return self.connection.commit()

    def __del__(self):
        self.connection.close()


@auth.get_password
def get_password_and_key(username):
    """ Simple text-based authentication """
    if username == '<user-name>':
        api_key = '<api-key>'
        return api_key
    else:
        return None


@auth.error_handler
def unauthorized():
    """
    Return a 403 instead of a 401 to prevent browsers from displaying
    the default auth dialog
    :param:
    :return: unauthorized message
    """
    return make_response(jsonify({'message': 'Unauthorized Access'}), 403)


task_fields = {
    'id': fields.Integer,
    'task_id': fields.Integer,
    'task_name': fields.String,
    'task_description': fields.String,
    'task_date': fields.DateTime,
    'task_due': fields.DateTime,
    'task_completed': fields.Boolean,
    'task_reminder': fields.Boolen,
    'task_userid': fields.Integer,
    'uri': fields.Url('task')
}


class TaskListAPI(Resource):
    """
    API Resource for listing all tasks from the database.
    Provides the endpoint for creating new tasks
    :param: none
    :type a json object
    :return task, status_code
    """
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type=int, required=False,
                                   help='The API URL\'s ID of the task.')
        self.reqparse.add_argument('task_id', type=int, required=False,
                                   help='The task ID field is an auto-incrementing database field')
        self.reqparse.add_argument('task_name', type=str, required=True,
                                   help='The name for the task.')
        self.reqparse.add_argument('task_description', type=str, required=False,
                                   help='The description for the task.')
        self.reqparse.add_argument('task_date', type=str, required=True,
                                   help='The date the task is created.')
        self.reqparse.add_argument('task_due', type=str, required=True,
                                   help='The task due date.')
        self.reqparse.add_argument('task_reminder', type=bool, required=False,
                                   help='Has the task reminder been sent.')
        self.reqparse.add_argument('task_completed', type=bool, required=False,
                                   help='Has the task been completed.')
        self.reqparse.add_argument('task_userid', type=int, required=True,
                                   help='The users ID the task belongs to.')
        self.reqparse.add_argument('uri', type=str, required=False,
                                   help='The full URL path of the stat.')

        super(TaskListAPI, self).__init__()

    def get(self):
        try:
            sql = u"select task_id, task_name, task_description, task_date, task_due, task_reminder, task_completed, " \
                  u"task_userid from tasks " \
                  u"WHERE task_date > ?"
            conn = AzureSQLDatabase()
            params = '12-1-2016'
            cursor = conn.query(sql, params)
            columns = [column[0] for column in cursor.description]
            tasks = []
            for row in cursor.fetchall():
                tasks.append(dict(zip(columns, row)))

            return {
                'tasks': marshal(tasks, task_fields)
            }

        except Exception as e:
            return {'error': str(e)}

    def post(self):
        try:
            args = self.reqparse.parse_args()
            data = request.get_json()

            task = {
                'task_id': data['task_id'],
                'task_name': data['task_name'],
                'task_description': data['task_description'],
                'task_date': data['task_date'],
                'task_due': data['task_due'],
                'task_completed': data['task_completed'],
                'task_reminder': data['task_reminder'],
                'task_userid': data['task_userid']
            }

            conn = AzureSQLDatabase()
            conn.query("insert into tasks(task_name, task_description, task_date, task_due, task_completed, \
                        task_userid) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       [task['task_name'], task['task_description'], task['task_date'], task['task_due'], task['task_completed'], task['task_reminder'], task['task_userid']])

            conn.commit()

            return {
                'task': task
            }, 201

        except Exception as e:
            return {'error': str(e)}


class TaskAPI(Resource):
    """
    API Resource for retrieving, modifying, updating and deleting a single
    task, by ID.
    :param: task_id
    :return: task details by ID.
    """
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type=int, required=False,
                                   help='The API URL\'s ID of the task.')
        self.reqparse.add_argument('task_id', type=int, required=False,
                                   help='The task ID field is an auto-incrementing database field',
                                   location='args')
        self.reqparse.add_argument('task_name', type=str, required=True,
                                   help='The name of the user task.',
                                   location='args')
        self.reqparse.add_argument('task_description', type=str, required=False,
                                   help='The task description',
                                   location='args')
        self.reqparse.add_argument('task_date', type=str, required=True,
                                   help='The date the task was created.',
                                   location='args')
        self.reqparse.add_argument('task_due', type=str, required=True,
                                   help='The task due date.',
                                   location='args')
        self.reqparse.add_argument('task_completed', type=bool, required=False,
                                   help='Has the task been completed.',
                                   location='args')
        self.reqparse.add_argument('task_reminder', type=bool, required=False,
                                   help='Has the task reminder been sent?',
                                   location='args')
        self.reqparse.add_argument('task_userid', type=int, required=True,
                                   help='The user ID for the task.',
                                   location='args')
        self.reqparse.add_argument('uri', type='str', required=False,
                                   help='The full URL path to the requested resource')
        super(TaskAPI, self).__init__()

    def get(self, id):
        try:
            conn = AzureSQLDatabase()
            params = id
            sql = u"select task_id, task_name, task_description, task_date, task_due, task_reminder, task_completed, " \
                  u"task_userid" \
                  u"where task_id = ?"

            cursor = conn.query(sql, params)
            columns = [column[0] for column in cursor.description]
            task = []
            for row in cursor.fetchall():
                task.append(dict(zip(columns, row)))

            return {
                'task': marshal(task, task_fields)
            }, 200

        except Exception as e:
            return {'error': str(e)}

    def put(self, id):
        try:
            conn = AzureSQLDatabase()
            data = request.get_json()
            params = (data['task_name'], data['task_description'], data['task_date'], data['task_due'], data['task_completed'], data['task_reminder'], data['task_userid'], id)
            conn.query("update tasks set task_name = ?, task_description = ?, task_date = ?, task_due = ?, \
                        task_completed = ?,  task_reminder = ?, task_userid = ? where task_id = ?", params)

            conn.commit()

            return {
                'task': data
            }, 204

        except Exception as e:
            return {'error': str(e)}

    def delete(self, id):
        try:
            conn = AzureSQLDatabase()
            params = id
            sql = u"delete from tasks where task_id = ?"
            cursor = conn.query(sql, params)
            conn.commit()

            return {
                'result': True
            }, 204

        except Exception as e:
            return {'error': str(e)}


# register the API resources and define endpoints
api.add_resource(TaskListAPI, '/api/v1.0/tasks', endpoint='tasks')
api.add_resource(TaskAPI, '/api/v1.0/tasks/<int:id>', endpoint='task')

if __name__ == '__main__':
    app.run(
        debug=config.DEBUG,
        port=config.PORT
    )
