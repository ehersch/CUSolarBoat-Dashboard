import axios from 'axios'
import fs from 'fs'

function httpget(url) {
  axios.get(url)
    .then(response => {
      fs.writeFile('data.json', JSON.stringify(response.data), function (err) {
        if (err) {
          console.log(err);
        }
      });
    })
    .catch(error => {
      // keep this commented out to only display last three voltages
      // console.log(error);
    });
  fs.readFile("./data.json", (err, jsonString) => {
    if (err) {
      console.log("Error reading file from disk:", err);
      return;
    }
    try {
      const data = JSON.parse(jsonString);
      var index = (data.logs[data.logs.length - 1].Readings[data.logs[data.logs.length - 1].Readings.length - 1]);
      console.log("V1: ", index["V1"], "\nV2: ", index["V2"], "\nV3: ", index["V3"])

    } catch (err) {
      console.log(err);
    }
  });
}

httpget('http://0.0.0.0:4000/all-logs')
