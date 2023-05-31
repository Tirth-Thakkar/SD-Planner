import json
import datetime
from datetime import date
from __init__ import app, db
from sqlalchemy.exc import IntegrityError

class LeaderUser(db.Model):
    __tablename__ = 'userLeaderboard'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _score = db.Column(db.Integer, unique=False, nullable=False)
    _locations = db.Column(db.JSON, unique=False, nullable=False)
    _tot_distance = db.Column(db.Integer, unique=False, nullable=False)
    _calc_distance = db.Column(db.Integer, unique=False, nullable=False)
    _dateG = db.Column(db.Date)


    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, name, score, locations, tot_distance, calc_distance, dateG=date.today()):
        self._name = name    # variables with self prefix become part of the object, 
        self._score = score
        self._locations = locations
        self._tot_distance = tot_distance
        self._calc_distance = calc_distance
        self._dateG = dateG


    # a name getter method, extracts name from object
    @property
    def name(self):
        return self._name
    
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name
    
    # a getter method, extracts email from object
    @property
    def score(self):
        return self._score
    
    # a setter function, allows name to be updated after initial object creation
    @score.setter
    def score(self, score):
        self._score = score
    
    # a getter method, extracts email from object
    @property
    def locations(self):
        return self._locations
    
    # a setter function, allows name to be updated after initial object creation
    @locations.setter
    def locations(self, locations):
        self._locations = locations

    # a getter method, extracts email from object
    @property
    def tot_distance(self):
        return self._tot_distance
    
    # a setter function, allows name to be updated after initial object creation
    @tot_distance.setter
    def tot_distance(self, tot_distance):
        self._tot_distance = tot_distance

    # a getter method, extracts email from object
    @property
    def calc_distance(self):
        return self._tot_distance
    
    # a setter function, allows name to be updated after initial object creation
    @calc_distance.setter
    def tot_distance(self, tot_distance):
        self._tot_distance = tot_distance
    
    # Convert dos to a string
    @property
    def dateG(self):
        dateG_string = self._dateG.strftime('%m-%d-%Y')
        return dateG_string
    
    # Setter function
    @dateG.setter
    def dateG(self, dateG):
        self._dateG = dateG
    
   
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "score": self.score,
            "locations": self.locations,
            "tot_distance": self.tot_distance,
            "calc_distance": self.calc_distance,
            "dateG": self.dateG
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, name="", score=0,locations="",tot_distance=0,calc_distance=0):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if score > 0:
            self.score = score
        if len(locations) > 0:
            self.locations = locations
        if tot_distance > 0:
            self.tot_distance = tot_distance
        if calc_distance > 0:
            self.calc_distance = calc_distance
        
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


def initLeaderUsers():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        score1 = LeaderUser('Chester', 100, ["Balboa Park"], 15, 11, date(2023,5,29))
        score2 = LeaderUser('Bob', 200, ["Balboa Park", "Zoo", "Seaworld"], 20, 12, date(1999,4,20))
        score3 = LeaderUser('Jeff', 300, ["Coronado", "Ocean Beach", "Fashion Valley"], 18, 9, date(2023,3,13))
        score4 = LeaderUser('Tirth', 1, ["Costco", "Walmart", "Mission Bay", "Seaworld"], 11, 11, date(2023,1,1))

        leaders = [score1,score2,score3,score4]

        for leader in leaders:
            try:
                leader.create()
            except IntegrityError:
                db.session.remove()
                print(f"error try again later")
            