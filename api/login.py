import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.logins import Login

login_api = Blueprint('login_api', __name__,
                   url_prefix='/api/logins')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(login_api)

class LoginAPI:        
    class Cred(Resource):  # User API operation for Create and Read
        def post(self): # Create method
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate uid
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 400
            # look for password and dob
            password = body.get('password')

            ''' #1: Key code block, setup USER OBJECT '''
            uo = Login(uid=uid)
            
            ''' Additional garbage error checking '''
            # set password if provided
            if password is not None:
                uo.set_password(password)
            # convert to date type
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            login = uo.create()
            # success returns json of user
            if login:
                return jsonify(login.read())
            # failure returns error
            return {'message': f'Processed {uid}, either a format error or User ID {uid} is duplicate'}, 400

        def get(self): # Read Method
            logins = Login.query.all()    # read/extract all users from database
            json_ready = [login.read() for login in logins]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
    
    class Search(Resource):

        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Get Data '''
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 400
            password = body.get('password')
            
            ''' Find user '''
            login = Login.query.filter_by(_uid=uid).first()
            if login is None or not login.is_password(password):
                return {'message': f"Invalid user id or password"}, 400
            
            ''' authenticated user '''
            return jsonify(login.read())

            

    # building RESTapi endpoint
    api.add_resource(Cred, '/logins')
    api.add_resource(Search, '/lsearch')
    