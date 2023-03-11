const axios = require('axios');
const fs = require('fs');
/*used to request data from the url as type ...*/
function httpget(url) {
  axios.get(url)
    .then(response => {
      fs.writeFile('data.json', getLastThree(JSON.stringify(response.data)), function (err) {
        if (err) {
          console.log(err);
        } else {
          console.log('Data written to file');
        }
      });
    })
    .catch(error => {
      console.log(error);
    });
}

function getLastThree(data) {
  var data1 = JSON.parse(data);
  var length = data1
}

httpget('http://0.0.0.0:4000/all-logs')
