from serial import Serial
import json
import time
from datetime import datetime
#s = Serial(port='/dev/cu.usbmodem11101', baudrate=9600)
s = Serial(port='COM4', baudrate=9600, timeout=.1)
from db import db
from db import Logs
from db import Readings
from sqlalchemy.sql.expression import func
from flask import Flask
import json
from flask import request
# pprint library is used to make the output look more pretty
from pprint import pprint
s.flushInput()
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

while True:
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

