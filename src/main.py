"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints t43334
"""
import os
import json
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets,People
#from models import Person
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
jwt = JWTManager(app)



@app.route("/users",methods=['GET'])
def all_users():
    people = User.get_all()
    people_dic = []
    for person in people :
        people_dic.append(person.serialize())
    return jsonify(people_dic),200

@app.route("/people",methods=['GET'])
def all_people():
    people = People.get_all()
    people_dic = []
    for person in people :
        people_dic.append(person.serialize())
    return jsonify(people_dic)

@app.route("/people",methods=['POST'])
def create_people ():
    json = request.get_json()
    people = People()
    people.set_with_json(json)
    people.db_post()
    return jsonify(people.serialize())

@app.route("/people/<int:people_id>", methods=['GET'])
def one_people(people_id):
    people = People.get_one_by_id(people_id)
    people_serialized = people.serialized()
    return jsonify(people_serialized)

@app.route("/people/<int:people_id>", methods=['DELETE'])
def delte_one_people(people_id):
    people = People.query.get(people_id)
    db.session.delete(people)
    db.session.commit()
    return jsonify(people.serialize(), "msg: User is deleted") 

@app.route("/people" , methods=["DELETE"])
def delete_all_person():
    people = People.get_all()
    print(people)


@app.route("/planets", methods=["GET"])

def all_planets():
    planets = Planets.get_all()
    planets_dic = []
    for planet in planets :
        planets_dic.append(planet.serialize())
    return jsonify(planets_dic)

@app.route("/planets",methods=['POST'])
def create_planet():
    json = request.get_json()
    planets = Planets()
    planets.set_with_json(json)
    planets.db_post()
    return jsonify(planets.serialize())

@app.route("/planet/<int:planet_id>", methods=['GET'])
def one_planet(planet_id):
    planet = People.get_one_by_id(planet_id)
    planet_serialized = planet.serialize()
    return jsonify(planet_serialized) 


@app.route("/login", methods=['POST'])
def handle_login():

    json=request.get_json()

    if json is None: 
        raise APIException("You shoulld be return a json")

    if "email" not in json:
        raise APIException("That's not an email in json")

    if "password" not in json:
        raise APIException("That's not a password in json")
    
    print(json["email"],json["password"])
   
    email = json["email"]
    password = json["password"]

    user = User.query.filter_by(email=email).one_or_none()

    if user is None:
         raise APIException("User not found")

    if not user.check_password(password):
      return jsonify("Your credentials are wrong, please try again"), 401

    access_token = create_access_token(identity=user.serialize())
    return jsonify(accessToken=access_token)






# @app.route("/profile", methods=['POST'])
# def handle_profile():
#     json = request.get_json()
#     user = User.user_have_token(json["token"])
#     if user is None :
#         raise APIExeption("You don't have a token")

#     return jsonify(user.serialize()),200

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

    


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200





# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
