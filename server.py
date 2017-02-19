from flask import Flask, request, jsonify
import hashlib
import uuid
import json
import time

app = Flask(__name__)



@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/register', methods = ['POST'])
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


@app.route('/api/enroll', methods = ['POST'])
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

@app.route('/api/login', methods = ['POST'])
def login():
	username = request.form['user']
	password = request.form['password']

	with open('login.json', 'r') as f:
		data = json.load(f)
		if username not in data:
			return 'Incorrect User'
		token = data[username]["token"]
	with open('register.json', 'r') as f:
		data = json.load(f)
		userInformation = data[token]
		passwordHash = userInformation['password_hash']
		if passwordHash != hashlib.md5(request.form['password']).hexdigest():
			return 'Incorrect Password'
		return token


@app.route('/api/addrequest', methods = ['POST'])
def addRequest():
	token = request.form['token']
	relation = request.form['relation']
	avail = request.form['avail']
	number = request.form['number']
	ethnicity = request.form['ethnicity']
	message = request.form['message']
	phno = request.form['phno']
	epoch = int(time.time())

	postJSON = {
		'token' : token,
		'relation' : relation,
		'avail' : avail,
		'number' : number,
		'ethnicity' : ethnicity,
		'message' : message,
		'phno' : phno,
		'status' : 'open',
		'epoch' : epoch
	}
	postHash = hashlib.md5(json.dumps(postJSON)).hexdigest()
	postJSON['posthash'] = postHash
	
	with open('posts.json', 'r') as f:
		try:
			data = json.load(f)
		except ValueError:
			data = {}
	
	with open('posts.json', 'w') as f:
		data[postHash] = postJSON
		json.dump(data, f)
	
	with open('register.json', 'r') as f:
		data = json.load(f)
		userinfo = data[token]
		userinfo['posthash'] = postHash

	with open('register.json', 'w') as f:
		data[token] = userinfo
		json.dump(data, f)
	return postHash


@app.route('/api/listposts', methods = ['GET'])
def listposts():
	with open('posts.json', 'r') as f:
		try:
			data = json.load(f)
		except:
			return '[]'
	posts = []
	for key,value in data.iteritems():
		if(value['status'] == 'open'):
			posts.append(value)
	posts = sorted(posts, key=lambda k: k['epoch'], reverse=True)
	return jsonify(posts)

@app.route('/api/acceptpost', methods = ['POST'])
def acceptpost():
	posthash = request.form['posthash']
	token = request.form['token']
	with open('posts.json', 'r') as f:
		data = json.load(f)
	with open('posts.json', 'w') as f:
		acceptedPost = data[posthash]
		acceptedPost['status'] = 'accepted'
		data[posthash] = acceptedPost
		json.dump(data, f)
	with open('register.json' , 'r') as f:
		data = json.load(f)
		userData = data[token]
		if 'acceptedpost' not in userData:
			userData['acceptedpost'] = []
		userData['acceptedpost'].append(acceptedPost)
	with open('register.json', 'w') as f:
		data[token] = userData
		json.dump(data, f)
	return 'OK'

@app.route('/api/listaccepted', methods = ['POST'])
def listaccepted():
	token = request.form['token']
	with open('register.json', 'r') as f:
		data = json.load(f)
		if 'acceptedpost' not in data[token]:
			return '[]'
		return jsonify(data[token]['acceptedpost'])

@app.route('/api/getlisting', methods = ['POST'])
def getlisting():
	token = request.form['token']
	with open('register.json', 'r') as f:
		try:
			data = json.load(f)
		except ValueError:
			data = {}
	
	with open('posts.json', 'r') as f:
		try:
			post = json.load(f)
		except ValueError:
			return 'null'
		if 'posthash' not in data[token]:
			return 'null'
		if data[token]['posthash'] not in post:
			return 'null'
		if post[data[token]['posthash']]['status'] == 'open':
			return jsonify(post[data[token]['posthash']])
		else:
			return null


#@app.route('/api/deletepost'


if __name__ == '__main__':
	      app.run(host='0.0.0.0', port=80)		
