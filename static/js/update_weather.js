function updateWeatherCurrent() {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
          document.getElementById("current-weather-box").innerHTML = xhr.response;
        }
    };
    xhr.open("GET", "/weather-current", true);
    xhr.send();
  }

function updateWeatherHourly() {
var xhr = new XMLHttpRequest();
xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 && xhr.status === 200) {
        document.getElementById("weather-forecast-hourly").innerHTML = xhr.response;
    }
};
xhr.open("GET", "/weather-hourly", true);
xhr.send();
}

function updateWeatherDaily() {
var xhr = new XMLHttpRequest();
xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 && xhr.status === 200) {
        document.getElementById("weather-forecast-daily").innerHTML = xhr.response;
    }
};
xhr.open("GET", "/weather-daily", true);
xhr.send();
}
  
// Initial call to update functions
updateWeatherCurrent();
updateWeatherHourly();
updateWeatherDaily();

// Set intervals to call update functions periodically
setInterval(updateWeatherCurrent, 30 * 60 * 1000); // Call updateWeatherCurrent every 30 minutes
setInterval(updateWeatherHourly, 60 * 60 * 1000); // Call updateWeatherHourly every hour
setInterval(updateWeatherDaily, 6 * 60 * 60 * 1000); // Call updateWeatherDaily every 6 hours
  