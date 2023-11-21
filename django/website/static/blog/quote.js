var getAQuoteForm = document.getElementById("get-a-quote-form");
var budget = document.getElementById("budget");

getAQuoteForm.addEventListener("submit", function (e) {
  e.preventDefault();
  validateForm();

  var marketing = Object.fromEntries(new URLSearchParams(window.location.search));
  var data = Object.fromEntries(new FormData(e.target).entries());

  var body = {
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
        window.gtag("event", "lead_created", {
          currency: "USD",
          budgetAmount: budget.value,
        });
      }
    })
    .catch(console.error);
});


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
  if (!phoneNumberInput.value.trim()) {
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