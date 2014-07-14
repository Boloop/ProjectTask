from flask import Flask
from flask import request
from sqlalchemy import create_engine
from datetime import datetime

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
		um = UserMan(ses)
		submitdata = request.form
		userToAdd = request.form.get('user', '')
		if not um.isUsernameValid(userToAdd):
			ses.close()
			return "Invalid Username"

		#Search the DB for a duplicate?
		dbUser = um.getUserByName(userToAdd)
		if dbUser != None:
			ses.close()
			return "User "+userToAdd+" already exists";
		#Otherwise add the user!
		
		um.addNewUser(userToAdd)
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

@app.route('/tasks/addtask', methods=['GET', 'POST'])
def userAddTask():
	ses = db.GetSession()
	um = UserMan(ses)
	if request.method == 'POST':
		submitdata = request.form
		taskNameToAdd = request.form.get('taskname', '')
		userAddedBy = request.form.get('username', '')
		if userAddedBy == "":
			ses.close()
			return "Could not add blank user"
		if taskNameToAdd == "":
			ses.close()
			return "Could not add blank task"

		#Search the DB for a duplicate?
		dbUser = ses.query(User).filter_by(name=userAddedBy).first()
		if dbUser == None :
			ses.close()
			return "User "+userAddedBy+" does not exist";

		#Otherwise add task by this user!
		taskObjToAdd = Task()
		taskObjToAdd.createdBy = dbUser.id
		taskObjToAdd.dateAddedUTC= datetime.utcnow()
		taskObjToAdd.priority = 50
		taskObjToAdd.shortName = taskNameToAdd
		ses.add(taskObjToAdd)
		ses.commit()
		ses.close()

		return "Task Added!"
	else:
		result = """
		<form name="input" action="/tasks/addtask" method="post">
		task name: <input type="text" name="taskname"></br>
		"""
		result += '<select name="username">'
		for user in um.getAllUserNames():
			result += '<option value="'+user+'">'+user+'</option>'
		result += "</select></br>"
		result += """
		<input type="submit" value="Add Task">
		</form>
		"""
		ses.close()
		return result

if __name__ == "__main__":
	app.debug = True
	app.run()
