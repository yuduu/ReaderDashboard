function updateTime() {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            document.getElementById("current-time").innerHTML = xhr.responseText;
        }
    };
    xhr.open("GET", "/time", true);
    xhr.send();
}

updateTime(); // Call initially
setInterval(updateTime, 30000); // Call every 30 seconds
