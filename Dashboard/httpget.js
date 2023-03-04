/*used to request data from the url as type ...*/
function httpget(url) {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open("GET", url, false);
  xmlHttp.send(null);
  return xmlHttp.responseText;
}

Console.log(httpget("http://0.0.0.0:4000/all-logs"))