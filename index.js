//var MongoClient = require('mongodb').MongoClient;
import { MongoClient } from 'node_modules/mongodb'
var url = "mongodb+srv://CUSolarBoat:Cu2uiQrlwlfZG2gJ@cluster0.lkpux.mongodb.net/test";

MongoClient.connect(url, function(err, db) {
  if (err) throw err;
  var dbo = db.db("DB");
  dbo.collection("id").findOne({}).toArray(function(err, result) {
    if (err) throw err;
    document.getElementById("pV1").innerHTML = result.V1;
    document.getElementById("pV2").innerHTML = result.V2;
    document.getElementById("pV3").innerHTML = result.V3;
    document.getElementById("pV4").innerHTML = result.V4;
    document.getElementById("pC").innerHTML = result.Current;
    //console.log(result);
    db.close();
  });
});