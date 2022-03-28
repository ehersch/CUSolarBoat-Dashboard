from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient("mongodb+srv://CUSolarBoat:Cu2uiQrlwlfZG2gJ@cluster0.lkpux.mongodb.net/Test",tls=True, tlsAllowInvalidCertificates=True)
db=client.Test
# Issue the serverStatus command and print the results
serverStatusResult=db.command("serverStatus")
#pprint(serverStatusResult)
test = {
    "Time" : "16",
    "V1" : "1",
    "V2" : "1",
    "V3" : "1",
    "Current" : "1"
}
result = db.id.insert_one(test)