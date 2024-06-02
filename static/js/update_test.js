function updateNews() {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            const data = xhr.response;
            document.getElementById("news1").innerHTML = data.key1;
            document.getElementById("news2").innerHTML = data.key2;
        }
    };
    xhr.open("GET", "/test", true);
    xhr.responseType = 'json'; // Set responseType to 'json'
    xhr.send();
  }
  
  updateNews(); // Call initially
  setInterval(updateNews, 30000); // Call every 30 seconds
  