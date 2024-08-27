const telNumbers = document.querySelectorAll(".phoneNumber");

telNumbers.forEach((button) => {
  button.addEventListener("click", function () {
    window.location.href = "tel:" + button.textContent;
  });
});

function generateRandomUserId() {
  const randomNumber = Math.random().toString(36).substr(2, 9); // Random alphanumeric string
  const timestamp = Date.now().toString().substr(-4); // Last 4 digits of current timestamp
  return randomNumber + timestamp;
}

function setUserIdToLocalStorage() {
  localStorage.getItem("userId") ??
    localStorage.setItem("userId", generateRandomUserId());
}

function setUser() {
  const user = {
    landingPage: window.location.href,
    referrer: document.referrer,
  };

  localStorage.setItem("user", JSON.stringify(user));
}

document.addEventListener("DOMContentLoaded", () => {
  // Set User ID
  setUserIdToLocalStorage();

  // Set User
  localStorage.getItem("user") ?? setUser();
});
