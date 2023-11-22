const telephoneButton = document.getElementById('telephone-button');

telephoneButton.addEventListener('click', function() {
    const phoneNumber = telephoneButton.textContent;
    window.location.href = 'tel:' + phoneNumber.trim();
});