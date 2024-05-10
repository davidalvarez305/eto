const pagination = document.getElementById("page_navigation");
const filters = new URLSearchParams();

const clearButton = document.getElementById('clearButton');

clearButton.addEventListener('click', () => {
  var urlWithoutQueryString = window.location.origin + window.location.pathname;
  window.location.replace(urlWithoutQueryString);
});

// Get all page elements
const pageElements = pagination.querySelectorAll("a");

// Initialize the index of the currently selected element
let indexOfCurrentlySelectedElement = 0;

pagination.addEventListener("click", function (e) {
    const target = e.target;

    // Handle clicking on number or chevron
    if (target.tagName === "A" || target.tagName === "DIV" || target.tagName === "svg") {
        let pageValue;

        // If clicking on number
        if (target.tagName === "A") {
            pageValue = parseInt(target.textContent.trim());
        }

        // If clicking on chevron
        if (target.tagName === "DIV" || target.tagName === "svg") {
            const chevronValue = target.getAttribute('data-chevron-value');

            if (chevronValue === "left_chevron") {
                if (indexOfCurrentlySelectedElement === 0) return;
                indexOfCurrentlySelectedElement -= 1;
            } else if (chevronValue === "right_chevron") {
                const maxPages = parseInt(JSON.parse(document.getElementById('max-pages').textContent));
                if (indexOfCurrentlySelectedElement === maxPages - 1) return;
                indexOfCurrentlySelectedElement += 1;
            }

            const indexedElement = pageElements[indexOfCurrentlySelectedElement];

            if (!indexedElement) return;

            pageValue = parseInt(indexedElement.textContent.trim());
        }

        // Get the base URL
        const baseUrl = window.location.href;

        // Set the "page" parameter in the URLSearchParams object
        if (pageValue) filters.set("page", pageValue);

        // Construct the final URL with search parameters
        const finalUrl = new URL(baseUrl);
        finalUrl.search = filters.toString();

        // Redirect to the final URL
        window.location.replace(finalUrl.toString());
    }
});

// Filtering logic
const filtersForm = document.getElementById("filters_form");

filtersForm.addEventListener("submit", function(e) {
    e.preventDefault();

    let values = {};
    const entry = Object.fromEntries(new FormData(e.target));
    for (const [key, value] of Object.entries(entry)) {
        if (value.length > 0) values[key] = value;
    }

    const qs = new URLSearchParams(values);

    const { origin, pathname } = window.location;
  
    const url = new URL(origin + pathname);

    url.search = qs.toString();

    window.location.replace(url.href);
});

const buttons = document.querySelectorAll('button[data-lead-id]');

buttons.forEach(button => {
  const leadId = button.getAttribute('data-lead-id');
  const photosCount = button.getAttribute('data-lead-photos');

  if (parseInt(photosCount) === 0) {
    button.disabled = true
    button.textContent = "N/A";
  }

  const imagesSlider = document.getElementById('imagesSlider');
  const imagesModalContainer = document.getElementById('imagesModalContainer');
  
  button.addEventListener('click', function() {
    const photos_dict = JSON.parse(document.getElementById('photos_dict').textContent);
    const bucket_url = JSON.parse(document.getElementById('bucket_url').textContent);
    const lead_images = photos_dict[leadId];

    imagesModalContainer.style.display = "";
    
    lead_images.forEach(image => {
      const containerDiv = document.createElement('div');
      const imgElement = document.createElement('img');

      imgElement.src = bucket_url + image;

      containerDiv.appendChild(imgElement);
      imagesSlider.appendChild(containerDiv);
    });

    $('#imagesSlider').slick({
      infinite: true,
      speed: 300,
      slidesToShow: 1,
      adaptiveHeight: true,
    });
  });
});

const closeModal = document.getElementById('closeModal');

closeModal.addEventListener("click", e => {
  $('#imagesSlider').slick('unslick');
  imagesModalContainer.style.display = "none";
});

const sliderPrevious = document.getElementById('sliderPrevious');
const sliderNext = document.getElementById('sliderNext');

sliderNext.addEventListener("click", () => $('#imagesSlider').slick('slickNext'));
sliderPrevious.addEventListener("click", () => $('#imagesSlider').slick('slickPrev'));


// User language modifier
const userLanguage = document.querySelectorAll(".userLanguage");

userLanguage.forEach(lang => {
  if (lang.textContent.trim() === "es-US") lang.textContent = "Español";
  if (lang.textContent.trim() === "en-US") lang.textContent = "English";
});

// Preserve querystring during pagination
var paginationAnchor = document.querySelectorAll('.paginationAnchor');
paginationAnchor.forEach(link => {
    link.addEventListener('click', event => {
        event.preventDefault();

        var clickedPage = event.target.textContent;

        console.log(clickedPage);

        qs = new URLSearchParams(window.location.search);

        qs.set('page', clickedPage);

        console.log(qs.toString());

        const { origin, pathname } = window.location;

        const redirPage = new URL(origin + pathname);
        redirPage.search = qs.toString();

        window.location.replace(redirPage.href);
    });
});