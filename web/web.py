from flask import Flask
from sqlalchemy import create_engine

import DataEngine

app = Flask(__name__)

db = DataEngine.DB()
db.Ignition()


@app.route("/")
def hello():
	result = "Running"
	ses = db.GetSession()
	return result

if __name__ == "__main__":
    app.run()
