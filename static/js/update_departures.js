function updateDepartures() {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            document.getElementById("departures").innerHTML = xhr.responseText;
        }
    };
    xhr.open("GET", "/departures", true);
    xhr.send();
}

updateDepartures(); // Call initially
setInterval(updateDepartures, 60000); // Call every 30 seconds
