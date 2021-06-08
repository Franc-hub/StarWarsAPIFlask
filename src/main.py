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

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

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
    people = People.get_one(people_id)
    people_serialized = people.serialized()
    return jsonify(people_serialized)

# @app.route("/planets",methods=['GET'])
# def all_planets():
# return jsonify(planets)

# @app.route("/planets/<int:planet_id>", methods=['GET'])
# def one_planet(planet_id):
# return jsonify(planets[planet_id])


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



# @app.route('/login',methods=['POST'])
# def handel_login():
#     json = reques.

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
