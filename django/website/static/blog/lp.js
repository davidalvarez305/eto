const startButton = document.getElementById("get-started-button");
const bottomCTAButton = document.getElementById("bottom-cta-button");
const popUpModalButton = document.getElementById("pop-up-modal-button");

const qs = new URLSearchParams(window.location.search);
const latitude = 0.0;
const longitude = 0.0;

document.addEventListener('DOMContentLoaded', getUserLocation())

function getLeadChannel() {

  // No referrer means the user accessed the website directly
  if (document.referrer.length === 0) return "direct";

  // If we get to this point, it means that document.referrer is not empty
  if (qs.entries.length === 0) return "organic";

  // Google Ads
  if (qs.get("gclid") !== null) return "paid";

  return "other";
};

function getUserLocation() {
  const options = {
    enableHighAccuracy: true,
    timeout: 3000,
    maximumAge: 0,
  };

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      function(position) {
        // Success callback
        latitude = position.coords.latitude;
        longitude = position.coords.longitude;
      },
      function(error) {
        console.error("Error getting user location:", error.message);
      },
      options
    );
  } else {
    console.error("Geolocation is not supported by your browser.");
  }
}

function getUserDeviceInfo() {
  const { userAgent, language } = navigator;
  return { userAgent, language };
}

function handleCTAClick(e) {
  const { userAgent, language } = getUserDeviceInfo();

  const clickedButtonId = e.target.id;
  // This set method must be first in order for the getLeadChannel logic to work correctly
  // Because it checks that all qs.entries are of length 0 ('meaning organic traffic')
  // It also checks document.referrer to differentiate direct vs organic
  qs.set('lead_channel', getLeadChannel());
  qs.set('referrer', document.referrer);
  qs.set('landing_page', window.location.href);
  qs.set('button_clicked', clickedButtonId);
  qs.set('longitude', longitude);
  qs.set('latitude', latitude);
  qs.set('userAgent', userAgent);
  qs.set('language', language);

  const currentDomain = new URL(window.location.protocol + "//" + window.location.host);

  window.location.replace(currentDomain.href + "quote?" + qs.toString());
};

startButton.addEventListener("click", handleCTAClick);
bottomCTAButton.addEventListener("click", handleCTAClick);
popUpModalButton.addEventListener("click", handleCTAClick);