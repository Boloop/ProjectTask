from flask import Flask
from flask import request
from sqlalchemy import create_engine

from DataEngine import *

app = Flask(__name__)

db = DB()
db.Ignition()


@app.route("/")
def index():
	result = "Running"
	ses = db.GetSession()
	users = ses.query(User)
	for user in users:
		result += "\n "+user.name
	ses.close()	
	return result


@app.route('/user/<username>')
def showUser(username):
	# show the user profile for that user
	result = "Running"
	ses = db.GetSession()
	user = ses.query(User).filter_by(name=username).first()
	if user != None:
		result += "\n "+user.name
	else:
		result += "Failed to find name"
	ses.close()	
	return result

@app.route('/admin/')
def adminIndex():
	result = "Admin Index"
	return result

@app.route('/admin/adduser', methods=['GET', 'POST'])
def adminAddUser():
	if request.method == 'POST':
		ses = db.GetSession()
		submitdata = request.form
		userToAdd = request.form.get('user', '')
		if userToAdd == "":
			ses.close()
			return "Could not add blank user"

		#Search the DB for a duplicate?
		dbUser = ses.query(User).filter_by(name=userToAdd).first()
		if dbUser != None:
			ses.close()
			return "User "+userToAdd+" already exists";
		#Otherwise add the user!
		userObjToAdd = User()
		userObjToAdd.name = userToAdd
		ses.add(userObjToAdd)
		ses.commit()
		ses.close()

		return "User Added!"
	else:
		return """
		<form name="input" action="/admin/adduser" method="post">
		user: <input type="text" name="user">
		<input type="submit" value="Add User">
		</form>
		"""

if __name__ == "__main__":
    app.run()
