from serial import Serial
import json
from datetime import datetime
s = Serial(port='/dev/cu.usbmodem11101', baudrate=9600)
from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
s.flushInput()
client = MongoClient("mongodb+srv://CUSolarBoat:Cu2uiQrlwlfZG2gJ@cluster0.lkpux.mongodb.net/test",tls=True, tlsAllowInvalidCertificates=True)
db=client.DB
logDic = {}
logDic["log"] = json.loads(json.dumps(list(db.id.find({}, {'_id': False, "Timestamp":False}))))
logDic["Timestamp"] = str(datetime.now())
db.logs.insert_one(logDic)
db["id"].drop()
timeIndex = 0
        # Issue the serverStatus command and print the results
serverStatusResult=db.command("serverStatus")

while True:
    try:
        ser_bytes = str(s.readline())
        ser_bytes = ser_bytes[3:len(ser_bytes) - 6]
       # print(ser_bytes)
        voltages = ser_bytes.split(", ")
        voltageDic = {}
        voltageDic["Index"] = timeIndex
        timeIndex += 1
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
        result = db.id.insert_one(voltageDic)
        #print(voltages)
    except Exception as e:
        
        print(e)
        #print("Keyboard Interrupt")
        break

