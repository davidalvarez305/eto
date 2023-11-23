const pagination = document.getElementById("page_navigation");
const filters = new URLSearchParams();

// Currently selected element
const pageValues = pagination.getElementsByTagName("a");
let indexOfCurrentlySelectedElement = 0;
let pageValue = "";

pagination.addEventListener("click", function (e) {
  const target = e.target;
  // Handle clicking on number
  if (target.tagName === "A") {
    pageValue = target.textContent.trim();
  }

  // Handle clicking on left/right chevron
  if (target.tagName === "DIV" || target.tagName === "svg") {
    const chevronValue = target.getAttribute('data-chevron-value');

    if (chevronValue === "left_chevron") {
        if (indexOfCurrentlySelectedElement === 0) return;
        indexOfCurrentlySelectedElement -= 1;
    };

    if (chevronValue === "right_chevron") {
        let maxPagesNum = parseInt(JSON.parse(document.getElementById('max-pages').textContent));

        const isMaxNumPages = parseInt(pageValues.item(indexOfCurrentlySelectedElement).textContent) === maxPagesNum
        if (isMaxNumPages) return;

        indexOfCurrentlySelectedElement += 1;
    };

    const el = pageValues.item(indexOfCurrentlySelectedElement);
    pageValue = el.textContent.trim();
  }

  // Perform GET request
  filters.set("page", pageValue);
  window.location.replace("/leads?" + filters.toString());
});

// Filtering logic
const filtersForm = document.getElementById("filters_form");

filtersForm.addEventListener("submit", function(e) {
    e.preventDefault();

    const values = Object.fromEntries(new FormData(e.target).entries());
    console.log(values);
});