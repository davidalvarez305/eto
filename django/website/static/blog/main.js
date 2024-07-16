const telephoneButton = document.getElementById("telephone-button");

telephoneButton.addEventListener("click", function () {
  const phoneNumber = telephoneButton.textContent.trim();
  window.location.href = "tel:" + phoneNumber;
});

function generateRandomUserId() {
  const randomNumber = Math.random().toString(36).substr(2, 9); // Random alphanumeric string
  const timestamp = Date.now().toString().substr(-4); // Last 4 digits of current timestamp
  return randomNumber + timestamp;
}

function setUserIdToLocalStorage() {
  const userId = localStorage.getItem("userId");

  if (userId !== null) return;

  const randomUserId = generateRandomUserId();

  localStorage.setItem("userId", randomUserId);
}

document.addEventListener("DOMContentLoaded", () => setUserIdToLocalStorage());
