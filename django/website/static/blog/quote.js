var getAQuoteForm = document.getElementById("get-a-quote-form");
var budget = document.getElementById("budget");

getAQuoteForm.addEventListener("submit", function (e) {
  e.preventDefault();
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
