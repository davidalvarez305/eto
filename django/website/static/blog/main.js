const telephoneButton = document.getElementById('telephone-button');

telephoneButton.addEventListener('click', function() {
    const phoneNumber = telephoneButton.textContent.trim();
    window.gtag('event', 'phone_click');
    window.location.href = 'tel:' + phoneNumber
});