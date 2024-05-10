const quoteButtons = document.querySelectorAll(".quoteButton");

const qs = new URLSearchParams(window.location.search);
let latitude = 0.0;
let longitude = 0.0;

document.addEventListener('DOMContentLoaded', getUserLocation())

function toTitleCase(str) {
  return str.replace(/\w\S*/g, function(txt) {
    return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
  });
}

function getHostFromURL() {
  const referrer = document.referrer;

  if (referrer.length === 0) return referrer;

  const parsedURL = new URL(document.referrer);

  const host = parsedURL.hostname.split('.')[1];;

  return host;
}

function getLeadChannel() {

  // No referrer means the user accessed the website directly
  if (document.referrer.length === 0) return "direct";

  // If we get to this point, it means that document.referrer is not empty
  if (qs.size === 0) {

    const host = getHostFromURL();

    qs.set('source', host);
    qs.set('medium', `${toTitleCase(host)} - SEO`);

    return "organic";
  }

  // Google Ads
  if (qs.has("gclid") || qs.has("msclkid")) return "paid";

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
  const language = navigator.language || navigator.userLanguage;
  const userAgent = navigator.userAgent;
  return { userAgent, language };
}

function handleCTAClick(e) {
  const { userAgent, language } = getUserDeviceInfo();

  const buttonName = e.target.getAttribute('name');
  // This set method must be first in order for the getLeadChannel logic to work correctly
  // Because it checks that all qs.entries are of length 0 ('meaning organic traffic')
  // It also checks document.referrer to differentiate direct vs organic
  qs.set('channel', getLeadChannel());
  qs.set('referrer', document.referrer);
  qs.set('landing_page', window.location.href);
  qs.set('button_clicked', buttonName);
  qs.set('longitude', longitude);
  qs.set('latitude', latitude);
  qs.set('userAgent', userAgent);
  qs.set('language', language);

  const currentDomain = new URL(window.location.origin + "/quote");

  currentDomain.search = qs.toString();

  window.location.replace(currentDomain.href);
};

quoteButtons.forEach(button => {
  let children = button.children;
  console.log(button.name);
  Array.from(children).forEach(child => {
      child.setAttribute("name", button.name);
  });

  button.addEventListener("click", handleCTAClick);
});