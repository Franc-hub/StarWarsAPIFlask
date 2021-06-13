from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Text, Boolean, Column
# from sqlalchemy.orm import deferred


db = SQLAlchemy()

class BaseModel():
    @classmethod
    def get_all(cls):
        return cls.query.all()
        

    @classmethod
    def get_one_by_id(cls,model_id):
        return cls.query.filter_by(id = model_id).first()


    @classmethod 
    def delete_all(cls):
        return cls.query.delete()
        

class User(db.Model,BaseModel):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name =Column(String(250))
    last_name =Column(String(250))
    email=Column(String(250), nullable=False)
    password=Column(String(250), nullable=False)
    is_logged=Column(Boolean, default=False, nullable=False)
    token = Column(String(250), nullable=True)
    favorite_planets = db.relationship('Favorite_Planet', backref='user', lazy=True)


    @staticmethod
    def login_credentials(email,password):
        return User.query.filter_by(email=email).filter_by(password=password).first()

    
    def have_token(self,token):
        self.token = token
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "token":self.token,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            "is_logged": self.is_logged,
            "favorite_planets": list(map(lambda x: x.serialize(), self.favorite_planets))
            # do not serialize the password, its a security breach
        }


class Planets(db.Model,BaseModel):
    __tablename__ = 'planets'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    population=Column(Integer,primary_key=False)
    orbital_period=Column(Integer,primary_key=False)
    rotation_period=Column(Integer,primary_key=False)
    diameter =Column(Integer,primary_key=False)
    favorite_planets = db.relationship('Favorite_Planet', backref='planets', lazy=True)
    

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name" : self.name,
            "population": self.population,
            "orbital_period" :self.orbital_period,
            "rotation_period" : self.rotation_period,
            "diameter": self.diameter 
            # do not serialize the password, its a security breach
        }

    

        
    def db_post(self):        
        db.session.add(self)
        db.session.commit()

    def set_with_json(self,json):
        self.name = json["name"]
        self.population = json["population"]
        self.orbital_period = json["orbital_period"]
        self.rotation_period = json["rotation_period"]
        self.diameter = json["diameter"]

    def db_delete(self):
        db.session.delete(self)
        db.session.commit()

        

    



class People(BaseModel,db.Model):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    eye_color=Column(String(250))
    skin_color=Column(String(250))
    gender=Column(String(250))
    height = Column(String(250))
    description= Column(String(250))
    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "eye_color":self.eye_color,
            "skin_color":self.skin_color,
            "gender":self.gender,
            "height":self.height,
            "description":self.description
            # do not serialize the password, its a security breach
        }
    
    def db_post(self):        
        db.session.add(self)
        db.session.commit()
    
    def set_with_json(self,json):
        self.name = json["name"]
        self.eye_color = json["eye_color"]
        self.skin_color = json["skin_color"]
        self.gender = json["gender"]
        self.height = json["height"]
        self.description = json["description"]



class Favorite_Planet(BaseModel,db.Model):
    __tablename__ = 'favorite_planet'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, db.ForeignKey('user.id'))
    planet_id = Column(Integer, db.ForeignKey('planets.id'))
    

    def __repr__(self):
        return '<Favorite_Planets %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id":self.planet_id,
            }

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(120), unique=True, nullable=False)
    done = db.Column(db.Boolean(), unique=False, nullable=False)