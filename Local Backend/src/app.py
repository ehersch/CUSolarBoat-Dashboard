from db import db
from db import Logs
from db import Readings
from sqlalchemy.sql.expression import func
from flask import Flask
import json
from flask import request

app = Flask(__name__)
db_filename = "Sysco.db"

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
#test route
@app.route("/")
def hello():
    return success_response(
        "Hello World"
    )

#get all logs route
@app.route("/all-logs")
def get_all_logs():
    return success_response(
        {"logs": [l.serialize() for l in Logs.query.all()]}
    )

#create a new log route
@app.route("/log", methods=["POST"])
def create_log():
    body = json.loads(request.data)
    if not body.get("time"):
        return failure_response("timestamp not provided!", 400)
    new_log = Logs(time= body.get("time"))
    db.session.add(new_log)
    db.session.commit()
    return success_response(new_log.serialize(), 201)

#get a specific log by its id route
@app.route("/log/<int:log_id>")
def get_log(log_id):
    log = Logs.query.filter_by(id=log_id).first()
    if log is None:
        return failure_response("Log not found!")
    return success_response(log.serialize())

# delete logs
@app.route("/log/<int:log_id>", methods=["DELETE"])
def delete_log(log_id):
    log = Logs.query.filter_by(id=log_id).first()
    if log is None:
        return failure_response("Log not found!")
    db.session.delete(log)
    db.session.commit()
    return success_response(log.serialize())

#get ALL readings route
@app.route("/all-readings")
def get_all_readings():
    return success_response(
        {"readings": [r.serialize() for r in Readings.query.all()]}
    )

#get specific reading by log_id and index route
@app.route("/reading/<int:log_id>/<int:reading_index>")
def get_reading(log_id, reading_index):
    reading = Readings.query.filter_by(log_id=log_id, index=reading_index).first()
    if reading is None:
        return failure_response("Reading not found!")
    return success_response(reading.serialize())

#create a reading and apend it to the most recent log route
@app.route("/reading", methods=["POST"])
def create_reading():
    body = json.loads(request.data)
    if not body.get("time") or not body.get("V1") or not body.get("V2") or not body.get("V3") or not body.get("C"):
        return failure_response("Required fields not provided!", 400)
    parent_log = Logs.query.filter_by(id=db.session.query(func.max(Logs.id))).first()
    if parent_log is None:
        return failure_response("No log to add to!")
    index = len(parent_log.Readings)
    log_id = parent_log.id
    new_reading = Readings(time= body.get("time"), V1=body.get("V1"), V2=body.get("V2"), V3=body.get("V3"), C=body.get("C"), index= index, log_id=log_id)
    parent_log.Readings.append(new_reading)
    db.session.add(new_reading)
    db.session.commit()
    return success_response(new_reading.serialize(), 201)

#delete specific reading by log_id and index route
@app.route("/reading/<int:log_id>/<int:reading_index>", methods=["DELETE"])
def delete_reading(log_id, reading_index):
    reading = Readings.query.filter_by(log_id=log_id, index=reading_index).first()
    if reading is None:
        return failure_response("Reading not found!")
    db.session.delete(reading)
    db.session.commit()
    return success_response(reading.serialize())

@app.route("/reset/")
def reset():
    db.drop_all()
    db.create_all()
    return success_response("yes")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)



