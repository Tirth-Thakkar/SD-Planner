from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building

from model.logins import Login

# Change variable name and API name and prefix
login_api = Blueprint('login_api', __name__,
                   url_prefix='/api/login')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(login_api)

class LoginAPI:     
    class AddLogin(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            email = body.get('email')
            if email is None or len(email) < 5:
                return {'message': f'Email is missing, or is less than 2 characters'}, 210
            password = body.get('password')

            ''' #1: Key code block, setup PLAYER OBJECT '''
            po = Login(email = email)
            
            ''' Additional garbage error checking '''
            # set password if provided
            if password is not None:
                po.set_password(password)            
            
            ''' #2: Key Code block to add user to database '''
            # create player in database
            login = po.create()
            # success returns json of player
            if login:
                return jsonify(login.read())
            # failure returns error
            return {'message': f'Processed {email}, either a format error or email is duplicate'}, 210
        
    class GetLogins(Resource):
        def get(self):
            logins = Login.query.all()    # read/extract all players from database
            json_ready = [login.read() for login in logins]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
        
    class UpdateLogin(Resource):
        def put(self):
            body = request.get_json() # get the body of the request
            data = body.get('data')
            email = body.get('email')
            login = Login.query.get(email) # get the player (using the uid in this case)
            login.update(data)
            return f"{login.read()} Updated"

    class DeleteLogin(Resource):
        def delete(self):
            body = request.get_json()
            email = body.get('email')
            login = Login.query.get(email)
            login.delete()
            return f"{login.read()} Has been deleted"


    # building RESTapi endpoint, method distinguishes action
    api.add_resource(AddLogin, '/score')
    api.add_resource(GetLogins, '/ulogin')
    api.add_resource(UpdateLogin, '/uplogin')
    api.add_resource(DeleteLogin, '/dlogin')   
