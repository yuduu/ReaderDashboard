function updateDate() {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            document.getElementById("current-date").innerHTML = xhr.responseText;
        }
    };
    xhr.open("GET", "/date", true);
    xhr.send();
}

updateDate(); // Call initially
setInterval(updateDate, 30000); // Call every 30 seconds
