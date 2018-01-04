""" 
This is the API for the james town app.
There is a Place and User tables, where the CRUD operation is applied on each.
"""

import os, sys, hashlib, uuid 

sys.path.append(os.getcwd())

from flask import Flask, render_template, redirect, session, request, jsonify
from models.jamestown_model import PlaceModel
from models.jamestown_model import UserModel
from models.base_model import DBSingelton

app = Flask(__name__)

@app.before_first_request
def initialize_tables():
	connect_db()
	if not PlaceModel.table_exists() :
		PlaceModel.create_table()
	if not UserModel.table_exists() :
		UserModel.create_table()

	disconnect_db()

@app.before_request
def connect_db():
	DBSingelton.getInstance().connect()

@app.teardown_request
def disconnect_db(err=None):
	if not DBSingelton.getInstance().is_closed():
		DBSingelton.getInstance().close()

@app.route('/')
def index():
	return "He is mine"

# curl -X POST -d "NameOfPlace=East Lagon&Description=This is the hub of the nation&long=123121&lat=321111&PhotoPlace=madina&PhotoQrcode=ncdwn323&PhoneNumberPlace1=321112121&PhoneNumberPlace2=44232322" localhost:5000/api/v1.0/place

#This function Creates a Place in the PlaceModel table. Fetches the data from a form and then inserts into the table.
@app.route("/api/v1.0/place", methods = ["POST"])
def create_place():
	NameOfPlace = request.form['NameOfPlace']
	Description = request.form['Description']
	GPS = [{'long':request.form['long']}, {'lat':request.form['lat']}]
	PhotoPlace = request.form['PhotoPlace']
	PhotoQrcode = request.form['PhotoQrcode']
	PhoneNumberPlace1 = request.form['PhoneNumberPlace1']
	PhoneNumberPlace2 = request.form['PhoneNumberPlace2']

	save_place = PlaceModel(NameOfPlace = NameOfPlace, Description = Description, GPS = GPS, PhotoPlace = PhotoPlace, PhotoQrcode = PhotoQrcode, PhoneNumberPlace1 = PhoneNumberPlace1, PhoneNumberPlace2 = PhoneNumberPlace2)
	save_place.save()

	success_message = "Added Successfully"
	return jsonify({"message":success_message})

#The GET request is used to fetch all the places from the database.
@app.route("/api/v1.0/place", methods = ["GET"])
def get_all_place():
	place = PlaceModel.select().order_by(PlaceModel.ID).dicts()
	return jsonify({'count':place.count()}, {'places':list(place)})

#The GET request is used to fetch a single place from the database.
@app.route("/api/v1.0/place/<int:place_id>", methods = ["GET"])
def get_a_place(place_id):
	place = PlaceModel.select().where(PlaceModel.ID == place_id).order_by(PlaceModel.ID).dicts()
	if len(place) == 0:
		success_message = "No record Found"
		return jsonify({"message":success_message})
	return jsonify({'count':place.count()}, {'places':list(place)})

#The DELETE request is used to delete a place from the database.
@app.route("/api/v1.0/place/<int:place_id>", methods = ["DELETE"])
def delete_a_place(place_id):
	place = PlaceModel.select().where(PlaceModel.ID == place_id)
	if len(place) != 0:
		place = PlaceModel.delete().where(PlaceModel.ID == place_id)
		place.execute()
		success_message = "Record deleted Successfully"
		return jsonify({"message":success_message})
	success_message = "No record Found"
	return jsonify({"message":success_message})

#The PUT request is used to update a single place in the table	
@app.route("/api/v1.0/place/<int:place_id>", methods = ['PUT'])
def update_place(place_id):
	place = PlaceModel.get(PlaceModel.ID == place_id)
	temp_place = place._data
	for key, value in temp_place.items():
		place._data[key] = request.form.get(key, value)
	place.save()
	success_message = "Successfully Updated record with ID {}".format(place_id)
	return jsonify({"message":success_message})

#The POST request is used here to create a user data and the hashlib is used to hash the password that is saved.
@app.route("/api/v1.0/user", methods = ['POST'])
def create_user():
	NameOfUser = request.form['NameOfUser']
	Email = request.form['Email']
	Password = request.form['Password']


	salt = uuid.uuid4().hex
	hashed_password = hashlib.sha512(Password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
	save_user = UserModel(NameOfUser = NameOfUser, Email = Email, Password = hashed_password)
	save_user.save()

	success_message = "Added Successfully"
	return jsonify({"message":success_message})

#This function gets all users in the user table
@app.route('/api/v1.0/user', methods = ['GET'])
def get_all_users():
	users = UserModel.select().order_by(UserModel.ID).dicts()
	if len(users) == 0:
		success_message = "No record Found"
		return jsonify({"message":success_message})
	return jsonify({'count':place.count()}, {'users':list(users)})

#This function gets a specific use in the user table
@app.route('/api/v1.0/user/<int:user_id>', methods = ['GET'])
def get_a_user(user_id):
	a_user = UserModel.select().where(UserModel.ID == user_id).dicts()
	if len(a_user) == 0:
		success_message = "No record Found"
		return jsonify({"message":success_message})
	return jsonify({'count':place.count()}, {'users':list(a_user)})

#This function deletes a specific user record
@app.route('/api/v1.0/user/<int:user_id>', methods = ['DELETE'])
def delete_a_user(user_id):
	a_user = UserModel.select().where(UserModel.ID == user_id)
	if len(a_user) != 0:
		a_user = UserModel.delete().where(UserModel.ID == user_id)
		a_user.execute()
		success_message = "Record deleted Successfully"
		return jsonify({"message":success_message})
	success_message = "No record Found"
	return jsonify({"message":success_message})

#This function makes it possible to edit a user record field
@app.route('/api/v1.0/user/<int:user_id>', methods = ['PUT'])
def update_user(user_id):
	user_data = UserModel.select().where(UserModel.ID == user_id)
	if len(user_data) == 0:
		success_message = "No record Found"
		return jsonify({"message":success_message})
	
	user_data = UserModel.get(UserModel.ID == user_id)
	user_temp = user_data._data
	
	for key, value in user_temp.items():
		user_data._data[key] = request.form.get(key, value)
	if request.form.get('Password'):
		salt = uuid.uuid4().hex
		Password_to_hash = str(request.form.get('Password'))
		hashed_password = hashlib.sha512(Password_to_hash.encode('utf-8') + salt.encode('utf-8')).hexdigest() 
		user_data._data['Password'] = hashed_password
	user_data.save()
	success_message = "Record Updated Successfully"
	return jsonify({"message":success_message})


