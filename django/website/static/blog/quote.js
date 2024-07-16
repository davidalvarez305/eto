const form = document.getElementById("get-a-quote-form");
const budget = document.getElementById("budget");
const alertModal = document.getElementById("alertModal");
const closeModalButton = document.getElementById("closeModal");
const fileInput = document.getElementById("file_upload");

function getUserIdFromLocalStorage() {
  const userId = localStorage.getItem("userId");
  if (!userId) {
    const randomUserId = generateRandomUserId();

    localStorage.setItem("userId", randomUserId);
  } else {
    return userId;
  }
}

function handleSubmitQuote(event) {
  event.preventDefault();
  const isValid = validateForm();

  if (!isValid) return;

  // Data inputs
  const marketing = Object.fromEntries(
    new URLSearchParams(window.location.search)
  );
  const body = new FormData(event.target);

  for (const key in marketing) {
    body.append(key, marketing[key]);
  }

  fetch("/quote", {
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
      const userId = getUserIdFromLocalStorage();

      let opts = { userId };

      let user = localStorage.getItem("user");

      if (user) {
        var data = JSON.parse(localStorage.getItem("user"));

        opts["landingPage"] = data.landingPage;
      }

      // Google Analytics
      window.gtag("event", "quote", { ...opts });

      alertModal.style.display = "";
      form.reset();
    })
    .catch(console.error);
}

closeModalButton.addEventListener(
  "click",
  () => (alertModal.style.display = "none")
);
form.addEventListener("submit", handleSubmitQuote);
