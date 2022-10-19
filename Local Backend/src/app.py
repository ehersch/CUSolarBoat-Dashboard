from db import db
from db import Logs
from db import Readings
from flask import Flask
import json
from flask import request

app = Flask(__name__)
db_filename = "cms.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

# generalized response formats
def success_response(data, code=200):
    return json.dumps(data), code


def failure_response(message, code=404):
    return json.dumps({"error": message}), code

# your routes here
@app.route("/")
def get_courses():
    return success_response(
        "Hello World"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
