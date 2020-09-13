import pyrebase

Fb_UN = ""
Fb_PW = ""
user = ""
firebase = ""
currentDevPath = ""
loginSuccess = False
def fbReadDb(path):
	global user
	global firebase
	db = firebase.database()
	val = db.child(path).get(user['idToken']).val()
	return(val)
def fbWriteDb(path,val):
	global user
	global firebase
	# Get a reference to the database service
	db = firebase.database()
	#----------------Update the Db with firmware image and Info
	try:
		results = db.child(path).set(val, user['idToken'])
	except:
		printE("Error: FB Db error")
def fbReadStorage(path):
	printD("")
def fbwriteStorage(path,val):
	#update in Storage
	global user
	global firebase
	storage = firebase.storage()
	try:
		storage.child(path).put(val, user['idToken']) #test1 is a path of file to beloaded and example.txt file name in database
	except:
		printE("Error: File read error or FB error")
	# wite to storage

def fbLogin(un,pw):
	global loginSuccess
	loginSuccess = False
	global Fb_UN 
	Fb_UN = un
	global Fb_PW 
	Fb_PW = pw
	global user
	global firebase
			### update OTA file
	config = {
			  "apiKey": "AIzaSyDvLY-epjfDOGKK7IoBe3rZ74ObUJcJpHo",
			  "authDomain": "cdmaster-f51fc.firebaseapp.com",
			  "databaseURL": "https://cdmaster-f51fc.firebaseio.com",
			  "storageBucket": "cdmaster-f51fc.appspot.com",
			  ###"serviceAccount": "path/to/serviceAccountCredentials.json" ### this is needed to autenticate as admin
			}
	
	firebase = pyrebase.initialize_app(config)

	# Get a reference to the auth service
	auth = firebase.auth()

	# Log the user in
	try:
		user = auth.sign_in_with_email_and_password(Fb_UN, Fb_PW)
		loginSuccess = True
	except:
		printE("Error: Login error")

def fbLoginSucess():
	return loginSuccess