import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import *
from flask_cors import cross_origin
from model.leaders1 import LeaderUser

leaderboard = Blueprint('leaderUser_api', __name__,
                   url_prefix='/api/leaderboardUser')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
leaders_api = Api(leaderboard)

class LeaderBoardAPI:        
    class AddScore(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented
        def post(self): # Create method
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            name = body.get('name')
            if name is None or len(name) < 1:
                return {'message': f'Name missing or too short'}, 400
            
            # validate uid
            score = int(body.get('score'))
            if score is None or score <= 0:
                return {'message': f'No username or score is too low'}, 400
            
            locations = body.get('locations')["list"]
            if locations is None or len(locations) <= 0:
                return {'message': f'No username or score is too low'}, 400
            
            tot_distance = int(body.get('tot_distance'))
            if tot_distance is None or tot_distance <= 0:
                return {'message': f'Total distance by user is nonexistnet or unrealistic'}, 400
            
            calc_distance = int(body.get('calc_distance'))
            if calc_distance is None or calc_distance <= 0:
                return {'message': f'Calculated distance is nonexistent or unrealistic'}, 400
            
            dateG = body.get('date')

            ''' #1: Key code block, setup USER OBJECT '''
            userMade = LeaderUser(name=name, score=score, locations=locations, tot_distance=tot_distance, calc_distance=calc_distance)

            # Checks if date of score exists, reformats it to mm-dd-yyyy
            if dateG is not None:
                try:
                    userMade.dateG = datetime.strptime(dateG, '%m-%d-%Y').date()
                except:
                    return {'message': f'Date obtained has a format error {dateG}, must be mm-dd-yyyy'}, 210
            
            user = userMade.create()
            # success returns json of user
            if user:
                return jsonify(user.read())
            # failure returns error
            return {'message': f'Processed {name}, either a format error or User ID {score} is duplicate'}, 400

    class LeaderGet(Resource):
        def get(self): # Read Method
            leaders = LeaderUser.query.all()    # read/extract all users from database
            json_ready = [leader.read() for leader in leaders]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

    # PUT method updates data in the API
    class LeaderUpdate(Resource):
        # def put(self) does the PUT method
        def put(self):
            # Gets the data from postman or frontend
            body = request.get_json()

            # Gets the username
            name = body.get('name')

            # Gets the score, score is going to be updated
            score = body.get('score')

            tot_distance = int(body.get('tot_distance'))
            
            calc_distance = int(body.get('calc_distance'))

            # Gets the user through the username
            userUpdating = LeaderUser.query.filter_by(_name = name).first()
            if userUpdating:
                # Updates the score for the user
                userUpdating.update(score = score)
                userUpdating.update(tot_distance = tot_distance)
                userUpdating.update(calc_distance = calc_distance)
                # Returns a dictionary to confirm that the score was updated
                return jsonify(userUpdating.read())
            else:
                # Error message if update fails
                return {'message': f'{name} not found'}, 210

    # Delete method deletes data in the API
    class LeaderDelete(Resource):
        # def delete(self) does the DELETE method
        def delete(self):
            # Gets the data from postman or frontend
            body = request.get_json()

            # Gets the ID
            getID = body.get('id')

            # Gets the user through the ID
            leaderDeleting = LeaderUser.query.get(getID)
            if leaderDeleting:
                # Deletes the user according to its ID number
                leaderDeleting.delete()
                return {'message': f'Profile #{getID} deleted'}, 210
            else:
                # Error message if delete fails
                return {'message': f'Profile #{getID} not found'}, 210


    class Search(Resource):
        def post(self):
            body = request.get_json()
            name = body.get('name')
            if name is None or len(name) < 1:
                return {'message': f'Name missing or too short'}, 400
            
            leaders = LeaderUser.query.order_by(LeaderUser._score.desc()).all()
            user_scores = [leader.read() for leader in leaders if leader._name == name]
            if len(user_scores) > 0:
                return jsonify(user_scores)
            else: 
                return {'message': f'No user found with name {name}'}, 400
            
    class GetUsersHighestScore(Resource):
        def get(self):
            leaders = LeaderUser.query.order_by(LeaderUser._score.desc()).all()
            json_ready = [leader.read() for leader in leaders]
            return jsonify(json_ready)
    
    
    # building RESTapi endpoint
    leaders_api.add_resource(AddScore, '/addscore')
    leaders_api.add_resource(LeaderGet, '/get')
    leaders_api.add_resource(LeaderUpdate, '/update')
    leaders_api.add_resource(LeaderDelete, '/delete')
    leaders_api.add_resource(Search, '/getSearch')
    leaders_api.add_resource(GetUsersHighestScore, '/getMaxScore')

    