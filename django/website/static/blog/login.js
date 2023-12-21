const form = document.getElementById("login-form");
const errorNotice = document.getElementById("login-error");
const rememberMe = document.getElementById("remember_me");
const username = document.getElementById("username");

// Fill in username if "rememberMe" exists in localStorage
document.addEventListener("DOMContentLoaded", function () {
  const username = localStorage.getItem("username");

  if (username) username.value = username;
});

form.addEventListener("submit", function (e) {
  e.preventDefault();

  const values = Object.fromEntries(new FormData(e.target));

  fetch("/login", {
    headers: {
      "X-CSRFToken": values.csrfmiddlewaretoken,
    },
    method: "POST",
    body: new FormData(e.target),
    credentials: "include",
  })
    .then((response) => response.json())
    .then(({ data }) => {
      if (data == "Authentication failed.") errorNotice.style.display = "";
      if (data == "Success.") window.location.replace("/leads");
    })
    .catch(console.error);
});

rememberMe.addEventListener("click", function (e) {
  if (username.innerHTML.length > 0 && e.target.checked)
    localStorage.setItem("username", username.value);
  if (!e.target.checked) localStorage.removeItem("username");
});