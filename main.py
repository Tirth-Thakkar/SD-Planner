import threading

# import "packages" from flask
from flask import render_template  # import render_template from "public" flask libraries
from flask_cors import CORS
# import "packages" from "this" project
from __init__ import app,db  # Definitions initialization
from model.jokes import initJokes
<<<<<<< HEAD
from model.logins import initLeaders
=======
# from model.users import initLeaders
>>>>>>> 4fb821d8417b4060e0d3d0bf9b4497af0fe1a7fd
from model.players import initPlayers
from model.leaders1 import initLeaderUsers

# setup APIs
from api.covid import covid_api # Blueprint import api definition
from api.joke import joke_api # Blueprint import api definition
from api.user import user_api # Blueprint import api definition
<<<<<<< HEAD
from api.login import player_api
from api.leaderboard import leaderboard
=======
from api.player import player_api
from api.leaderboard1 import leaderboard
>>>>>>> 4fb821d8417b4060e0d3d0bf9b4497af0fe1a7fd

# setup App pages
from projects.projects import app_projects # Blueprint directory import projects definition


# Initialize the SQLAlchemy object to work with the Flask app instance
db.init_app(app)

# register URIs
app.register_blueprint(joke_api) # register api routes
app.register_blueprint(covid_api) # register api routes
app.register_blueprint(user_api) # register api routes
app.register_blueprint(player_api)
app.register_blueprint(app_projects) # register app pages
app.register_blueprint(leaderboard)

@app.errorhandler(404)  # catch for URL not found
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/')  # connects default URL to index() function
def index():
    return render_template("index.html")

@app.route('/table/')  # connects /stub/ URL to stub() function
def table():
    return render_template("table.html")

@app.before_first_request
def activate_job():  # activate these items 
    initJokes()
    initLeaderUsers()
    initPlayers()

# this runs the application on the development server
if __name__ == "__main__":
    # change name for testing
    cors = CORS(app)
    app.run(debug=True, host="0.0.0.0", port="8086")
