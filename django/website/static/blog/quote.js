const getAQuoteForm = document.getElementById("get-a-quote-form");
const budget = document.getElementById("budget");

getAQuoteForm.addEventListener("submit", function (e) {
  e.preventDefault();
  const isValid = validateForm();

  if (!isValid) return;

  const marketing = Object.fromEntries(new URLSearchParams(window.location.search));
  const data = Object.fromEntries(new FormData(e.target).entries());

  const body = {
    ...marketing,
    ...data,
  };

  fetch("/quote", {
    headers: {
      "Content-Type": "application/json",
      'X-CSRFToken': data.csrfmiddlewaretoken,
    },
    method: "POST",
    credentials: "include",
    body: JSON.stringify(body),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.data) {
        // Send successful lead creation to Google Analytics
        const services = JSON.parse(document.getElementById('services').textContent);
        const locations = JSON.parse(document.getElementById('locations').textContent);

        let service = services.filter((service => service.id === parseInt(body['service'])))[0];
        let location = locations.filter((location => location.id === parseInt(body['location'])))[0];

        // Google Analytics
        window.gtag('event', 'quote', {
          'service': service.name,
          'location': location.name
        });

        // Google Ads
        window.gtag('event', 'conversion', {
          'send_to': 'AW-626941279/wOKxCI-S6_4YEN-6-aoC'
        });
      }
    })
    .catch(console.error);
});

function validatePhoneNumber(phoneNumberInput) {
  let isValid = true;
  const phoneNumber = phoneNumberInput.value.trim();

  const phonePattern = /^[0-9]{10}$/;

  if (!phonePattern.test(phoneNumber)) {
    isValid = false;
  }

  return isValid;
}

function validateForm() {
  let isValid = true;

  // Validate first name
  const firstNameInput = document.getElementById('first_name');
  if (!firstNameInput.value.trim()) {
      isValid = false;
  }

  // Validate last name
  const lastNameInput = document.getElementById('last_name');
  if (!lastNameInput.value.trim()) {
      isValid = false;
  }

  // Validate phone number
  const phoneNumberInput = document.getElementById('phone_number');
  if (!validatePhoneNumber(phoneNumberInput)) {
      isValid = false;
  }

  // Validate service
  const serviceSelect = document.getElementById('service');
  if (serviceSelect.value === '') {
      isValid = false;
  }

  // Validate location
  const locationSelect = document.getElementById('location');
  if (locationSelect.value === '') {
      isValid = false;
  }

  // Validate message
  const messageInput = document.getElementById('message');
  if (!messageInput.value.trim()) {
      isValid = false;
  }

  if (!isValid) {
    alert('Missing fields on form.');
  }

  return isValid;
}