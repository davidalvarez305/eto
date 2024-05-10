const telephoneButton = document.getElementById('telephone-button');

telephoneButton.addEventListener('click', function() {
    const phoneNumber = telephoneButton.textContent.trim();
    window.location.href = 'tel:' + phoneNumber
});

document.addEventListener("DOMContentLoaded", function() {
    var landingPage = localStorage.getItem("landingPage");
    if (!landingPage) {
        localStorage.setItem("landingPage", window.location.href);
    } else {
        document.referrer = landingPage;
    }
});