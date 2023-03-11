/*used to request data from the url as type ...*/
function httpget(url) {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open("GET", url, false);
  xmlHttp.send(null);
  return xmlHttp.responseText;
}

function getUrlVars(url) {
  var hash;
  var myJson = {};
  var hashes = url.slice(url.indexOf('?') + 1).split('&');
  for (var i = 0; i < hashes.length; i++) {
    hash = hashes[i].split('=');
    myJson[hash[0]] = hash[1];
    // If you want to get in native datatypes
    // myJson[hash[0]] = JSON.parse(hash[1]); 
  }
  return myJson;
}

var params = getUrlVars("http://0.0.0.0:4000/all-logs");
console.log(params);



//Console.log(httpget("http://0.0.0.0:4000/all-logs"))