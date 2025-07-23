function updateCompliment() {
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {
        requestAnimationFrame(() => {
          document.getElementById("compliment").textContent = xhr.response;
        });
      }
  };
  xhr.open("GET", "/compliment", true);
  xhr.send();
}

updateCompliment(); // Call initially
// Update only when display is active
let updateTimeout;
function scheduleUpdate() {
  updateCompliment();
  updateTimeout = setTimeout(scheduleUpdate, 24 * 60 * 60 * 1000); // Maintain 24h interval
}

// Initial update on document load
document.addEventListener('DOMContentLoaded', () => {
  requestIdleCallback(scheduleUpdate, { timeout: 1000 });
});

// Pause updates when document hidden
document.addEventListener('visibilitychange', () => {
  if (document.hidden) {
    clearTimeout(updateTimeout);
  } else {
    scheduleUpdate();
  }
});
