function updateWeather() {
  const xhr = new XMLHttpRequest();
  xhr.open('GET', '/weather');
  xhr.onload = function () {
      if (xhr.status === 200) {
          const data = JSON.parse(xhr.responseText);

          // Update current weather
          // Current Temp
          const currentWeatherDiv = document.getElementById('current-temp');
          if (currentWeatherDiv) {
              currentWeatherDiv.innerHTML = `${Math.round(data.current.temp)}°C`
          }
          // Current Icon
          const currentWeatherIco = document.getElementById('current-weather-ico');
          if (currentWeatherIco) {
              currentWeatherIco.innerHTML = `<i class="wi wi-owm-${data.current.weather[0].id}"></i>`;
          }
          // Current Feels Like
          const currentFeelsWeatherDiv = document.getElementById('current-feels-like-temp');
          if (currentFeelsWeatherDiv) {
              currentFeelsWeatherDiv.innerHTML = `${Math.round(data.current.feels_like)}°C`
          }
          // Update hourly forecast
          const hourlyForecastDivs = document.getElementById('weather-forecast-hourly');
          hourlyForecastDivs.innerHTML = ''; // Clear previous content
          for (let i = 1; i <= 11; i += 2) {
              hourlyForecastDivs.innerHTML += `<div class="box">
                  <div class="weather-forecast-hourly ">${data.hourly[i].dt}</div>
                  <div class="weather-forecast-hourly">${Math.round(data.hourly[i].temp)}°</div>
                  <div class="weather-forecast-hourly"><i class="wi wi-owm-${data.hourly[i].weather[0].id}"></i></div>
              </div>`;
          }

          // Update daily forecast
          const dailyForecastDivs = document.getElementById('weather-forecast-daily');
          dailyForecastDivs.innerHTML = ''; // Clear previous content
          for (let i = 1; i <= 5; i++) {
              dailyForecastDivs.innerHTML += `<div class="container border">
                  <div class="box">${data.daily[i].dt}</div>
                  <div class="box"><i class="wi wi-owm-${data.daily[i].weather[0].id}"></i></div>
                  <div class="box">${Math.round(data.daily[i].temp.min)}</div>
                  <div class="box">${Math.round(data.daily[i].temp.max)}</div>
              </div>`;
          }
      } else {
          console.error('Request failed. Status:', xhr.status);
      }
  };
  xhr.onerror = function () {
      console.error('Request failed');
  };
  xhr.send();
}

// Call the function to update weather on page load
updateWeather();
setInterval(updateWeather, 30 * 60 * 1000); // Call every 30 minutes in milliseconds
