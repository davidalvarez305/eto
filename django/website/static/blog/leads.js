const pagination = document.getElementById("page_navigation");
const filters = new URLSearchParams();

const clearButton = document.getElementById('clearButton');

clearButton.addEventListener('click', () => {
    window.location.replace("/leads");
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

            pageValue = parseInt(pageElements[indexOfCurrentlySelectedElement].textContent.trim());
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
    window.location.replace("/leads?" + qs.toString());
});

const buttons = document.querySelectorAll('button[data-lead-id]');

buttons.forEach(button => {
  const leadId = button.getAttribute('data-lead-id');
  const photosCount = button.getAttribute('data-lead-photos');

  if (parseInt(photosCount) === 0) {
    button.disabled = true
    button.textContent = "";
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