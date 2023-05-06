from serial import Serial
import json
import time
from datetime import datetime

from db import db
from db import Logs
from db import Readings
from sqlalchemy.sql.expression import func
from flask import Flask
import json
from flask import request
# pprint library is used to make the output look more pretty
from pprint import pprint
from db import BoolVal
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

# @app.route("/api/users/", methods=["POST"])
# def create_user():
#     body = json.loads(request.data)
#     if not body.get("name") or not body.get("netid"):
#         return failure_response("not all fields were provided!", 400)
#     new_user = User(name=body.get("name"), netid=body.get("netid"))
#     db.session.add(new_user)
#     db.session.commit()
#     return success_response(new_user.serialize(), 201)
#
# @app.route("/api/users/<int:user_id>/")
# def get_user(user_id):
#     user = User.query.filter_by(id=user_id).first()
#     if user is None:
#         return failure_response("User not found!")
#     return success_response(user.serialize())
#
# @app.route("/api/courses/<int:course_id>/add/", methods=["POST"])
# def add_user(course_id):
#     body = json.loads(request.data)
#     course = Course.query.filter_by(id=course_id).first()
#     if course is None:
#         return failure_response("Course not found!")
#     if not body.get("user_id"):
#         return failure_response("user not provided!", 400)
#     if body.get("type") != "student" and body.get("type") != "instructor":
#         return failure_response("invalid user type", 400)
#     user = User.query.filter_by(id=body.get("user_id")).first()
#     if user is None:
#         return failure_response("User not found!")
#     for person in course.students:
#         if person.id == user.id:
#             return failure_response("already in the class!", 400)
#     for person in course.instructors:
#         if person.id == user.id:
#             return failure_response("already in the class!", 400)
#     if body.get("type") == "student":
#         course.students.append(user)
#     if body.get("type") == "instructor":
#         course.instructors.append(user)
#     db.session.commit()
#     course = Course.query.filter_by(id=course_id).first()
#     return success_response(course.serialize())
#
# @app.route("/api/courses/<int:course_id>/assignment/", methods=["POST"])
# def add_assignment(course_id):
#     body = json.loads(request.data)
#     course = Course.query.filter_by(id=course_id).first()
#     if course is None:
#         return failure_response("Course not found!")
#     if not body.get("title") or not body.get("due_date"):
#         return failure_response("not all fields filled", 400)
#     assignment = Assignment(title=body.get("title"), due_date=body.get("due_date"), course_id=course_id)
#     course = Course.query.filter_by(id=course_id).first()
#     course.assignments.append(assignment)
#     db.session.add(assignment)
#     db.session.commit()
#     return success_response(assignment.serialize(), 201)
#
@app.route("/reset/")
def reset():
    db.drop_all()
    db.create_all()
    return success_response("yes")

@app.route("/stop/")
def stop():
    BoolVal.flag = False
    return success_response("yes")

@app.route("/collect/")
def collect():
    # s = Serial(port='/dev/cu.usbmodem1101', baudrate=9600)
    s = Serial(port='COM4', baudrate=9600, timeout=.1)
    s.flushInput()
    # Serial.close(s)
    new_log = Logs(time= str(datetime.now()))
    db.session.add(new_log)
    db.session.commit()
    parent_log = Logs.query.filter_by(id=db.session.query(func.max(Logs.id))).first()

    # client = MongoClient("mongodb+srv://CUSolarBoat:Cu2uiQrlwlfZG2gJ@cluster0.lkpux.mongodb.net/test",tls=True, tlsAllowInvalidCertificates=True)
    # db=client.DB
    # logDic = {}
    # logDic["log"] = json.loads(json.dumps(list(db.id.find({}, {'_id': False, "Timestamp":False}))))
    # logDic["Timestamp"] = str(datetime.now())
    # db.logs.insert_one(logDic)
    # db["id"].drop()
    # timeIndex = 0
    #         # Issue the serverStatus command and print the results
    # serverStatusResult=db.command("serverStatus")
    time.sleep(1)
    BoolVal.flag = True
    while BoolVal.flag:
        try:
            ser_bytes = str(s.readline())
            time.sleep(1)
            ser_bytes = ser_bytes[3:len(ser_bytes) - 6]
        # print(ser_bytes)
            voltages = ser_bytes.split(", ")
            voltageDic = {}
            voltageDic["Index"] = len(parent_log.Readings)
            for v in voltages:
                voltageDic[v[0:2]] = float(v[4:])
            #print(voltageDic['V1'])
            #voltageDic['V4'] = 0.0
            voltageDic['Current'] = 0.0
            voltageDic["Timestamp"] = str(datetime.now())
            
            # connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
            
            #pprint(serverStatusResult)
            '''
            test = {
                "Time" : "16",
                "V1" : "1",
                "V2" : "1",
                "V3" : "1",
                "V4" : "1",
                "Current" : "1"
            }'''
            new_reading = Readings(time= voltageDic.get("Timestamp"), V1=voltageDic.get("V1"), V2=voltageDic.get("V2"), V3=voltageDic.get("V3"), C=voltageDic.get("Current"), index= voltageDic.get("Index"), log_id=parent_log.id)
            parent_log.Readings.append(new_reading)
            db.session.add(new_reading)
            db.session.commit()
            #print(voltages)
        except Exception as e:
            
            print(e)
            #print("Keyboard Interrupt")
            break
    return success_response("yes")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)



