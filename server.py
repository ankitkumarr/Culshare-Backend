from flask import Flask, request, jsonify
import hashlib
import uuid
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/register', methods = ['POST'])
def register():
	name = request.form['name']
	userid = request.form['user']
	passwordhash = hashlib.md5(request.form['password']).hexdigest()
	token = uuid.uuid4().hex
	jsonInformationUser = {
		'name' : name,
		'username' : userid,
		'password_hash' : passwordhash
	}
	jsonInformationToken = {
		'token' : token
	}
		
	with open('register.json', 'r') as f:
		try:
			data = json.load(f)
		except ValueError:
			data = {}

	with open('register.json', 'w') as f:
		data[token] = jsonInformationUser
		json.dump(data, f)

	with open('login.json', 'r') as f:
		try:
			data = json.load(f)
		except ValueError:
			data = {}

	with open('login.json', 'w') as f:
		data[userid] = jsonInformationToken
		json.dump(data, f)

	return jsonify(token=token)


@app.route('/enroll', methods = ['POST'])
def enroll():
	token = request.form['token']
	ethnicity = request.form['ethnicity']
	age = request.form['age']

	with open('register.json', 'r') as f:
		data = json.load(f)
		userinfo = data[token]
		userinfo['ethnicity'] = ethnicity
		userinfo['age'] = age
	with open('register.json', 'w') as f:
		data[token] = userinfo
		json.dump(data, f)
	return 'OK'

@app.route('/login', methods = ['POST'])
def login():
	username = request.form['user']
	password = request.form['password']

	with open('login.json', 'r') as f:
		data = json.load(f)
		password

		
