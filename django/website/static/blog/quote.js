const getAQuoteForm = document.getElementById("get-a-quote-form");
const budget = document.getElementById("budget");
const alertModal = document.getElementById("alertModal");
const closeModalButton = document.getElementById("closeModal");
const fileInput = document.getElementById("file_upload");

closeModalButton.addEventListener("click", () => (alertModal.style.display = "none"));

getAQuoteForm.addEventListener("submit", e => {
  e.preventDefault();
  const isValid = validateForm();

  if (!isValid) return;

  // Data inputs
  const marketing = Object.fromEntries(new URLSearchParams(window.location.search));
  const body = new FormData(e.target);
  
  for (const key in marketing) {
    body.append(key, marketing[key]);
  }

  fetch("/quote", {
    headers: {
      "X-CSRFToken": body.get('csrfmiddlewaretoken'),
    },
    method: "POST",
    credentials: "include",
    body: body,
  })
    .then((response) => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error("Error: " + response.statusText);
      }
    })
    .then(() => {
      const clientId = UUID.generate();
      const services = JSON.parse(document.getElementById("services").textContent);
      const locations = JSON.parse(document.getElementById("locations").textContent);

      let service = services.find(service => service.id === parseInt(body["service"]));
      let location = locations.find(location => location.id === parseInt(body["location"]));

      // Google Analytics
      window.gtag("event", "quote", {
        service: service.name,
        location: location.name,
        event_id: clientId
      });

      alertModal.style.display = "";
      getAQuoteForm.reset();
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
  const firstNameInput = document.getElementById("first_name");
  if (!firstNameInput.value.trim()) {
    isValid = false;
  }

  // Validate last name
  const lastNameInput = document.getElementById("last_name");
  if (!lastNameInput.value.trim()) {
    isValid = false;
  }

  // Validate phone number
  const phoneNumberInput = document.getElementById("phone_number");
  if (!validatePhoneNumber(phoneNumberInput)) {
    isValid = false;
  }

  // Validate service
  const serviceSelect = document.getElementById("service");
  if (serviceSelect.value === "") {
    isValid = false;
  }

  // Validate location
  const locationSelect = document.getElementById("location");
  if (locationSelect.value === "") {
    isValid = false;
  }

  // Validate message
  const messageInput = document.getElementById("message");
  if (!messageInput.value.trim()) {
    isValid = false;
  }

  if (!isValid) {
    alert("Missing fields on form.");
  }

  return isValid;
}
