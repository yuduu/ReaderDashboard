function updateCompliment() {
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {
        document.getElementById("compliment").innerHTML = xhr.response;
      }
  };
  xhr.open("GET", "/compliment", true);
  xhr.send();
}

updateCompliment(); // Call initially
setInterval(updateCompliment, 24 * 60 * 60 * 1000); // 24h
