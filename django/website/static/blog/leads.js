const pagination = document.getElementById("page_navigation");
const filters = new URLSearchParams();

const normalClass = "hover:cursor-pointer -mr-px inline-flex items-center justify-center space-x-2 border border-gray-200 bg-white px-4 py-2 font-semibold leading-6 text-gray-800 hover:z-1 hover:border-gray-300 hover:text-gray-900 hover:shadow-sm focus:z-1 focus:ring focus:ring-gray-300 focus:ring-opacity-25 active:z-1 active:border-gray-200 active:shadow-none dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:border-gray-600 dark:hover:text-gray-200 dark:focus:ring-gray-600 dark:focus:ring-opacity-40 dark:active:border-gray-700";
const selectedClass = "hover:cursor-pointer -mr-px inline-flex items-center justify-center space-x-2 border border-gray-200 bg-gray-100 px-4 py-2 font-semibold leading-6 text-gray-800 hover:z-1 hover:border-gray-300 hover:text-gray-900 hover:shadow-sm focus:z-1 focus:ring focus:ring-gray-300 focus:ring-opacity-25 active:z-1 active:border-gray-200 active:shadow-none dark:border-gray-700 dark:bg-gray-700/75 dark:text-gray-300 dark:hover:border-gray-600 dark:hover:text-gray-200 dark:focus:ring-gray-600 dark:focus:ring-opacity-40 dark:active:border-gray-700";

// Currently selected element
let currentlySelectedElement = null;
let indexOfCurrentlySelectedElement = 0;
const pageValues = pagination.getElementsByTagName("a");

// Find currently selected element
for (let i = 0; i < pageValues.length; i++) {
    const el = pageValues[i];
    console.log(el.className);
    if (el.className === selectedClass) {
        currentlySelectedElement = el;
        indexOfCurrentlySelectedElement = i;
        break;
    }
}

pagination.addEventListener("click", function (e) {
  const target = e.target;
  // Handle clicking on number
  if (target.tagName === "A") {

    // Change selected element
    target.className = selectedClass;
    currentlySelectedElement.className = normalClass;
    currentlySelectedElement = target;
    const pageValue = target.textContent.trim();
    indexOfCurrentlySelectedElement = parseInt(pageValue) - 1;

    // Perform GET request
    filters.set("page", pageValue);

    fetch("/leads?" + filters.toString(), {
      headers: {
        "Content-Type": "application/json",
      },
      method: "GET",
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => console.log(data))
      .catch(console.error);
  }

  // Handle clicking on left/right chevron
  if (target.tagName === "DIV" || target.tagName === "svg") {
    const chevronValue = target.getAttribute('data-chevron-value');

    if (chevronValue === "left_chevron") {
        if (indexOfCurrentlySelectedElement === 0) return;

        indexOfCurrentlySelectedElement -= 1;

        // First switch the class of the current element
        currentlySelectedElement.className = normalClass;

        // Re-assignment & switch class
        currentlySelectedElement = pageValues.item([indexOfCurrentlySelectedElement]);
        currentlySelectedElement.className = selectedClass;
    };

    if (chevronValue === "right_chevron") {
        let maxPagesNum = parseInt(JSON.parse(document.getElementById('max-pages').textContent));
        // Make table elements programmatic
        // Get max value

        // Index will be -1 because it's a zero based value
        const isMaxNumPages = parseInt(pageValues.item(indexOfCurrentlySelectedElement).textContent) === maxPagesNum
        if (isMaxNumPages) return;

        indexOfCurrentlySelectedElement += 1;

        // First switch the class of the current element
        currentlySelectedElement.className = normalClass;

        // Re-assignment & switch class
        currentlySelectedElement = pageValues.item(indexOfCurrentlySelectedElement);
        currentlySelectedElement.className = selectedClass;
    };
  }
});

// Filtering logic
const filtersForm = document.getElementById("filters_form");

filtersForm.addEventListener("submit", function(e) {
    e.preventDefault();

    const values = Object.fromEntries(new FormData(e.target).entries());
    console.log(values);
});