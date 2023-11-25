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

  const imagesModalContainer = document.getElementById('imagesModalContainer');
  
  button.addEventListener('click', function() {
    const photos_dict = JSON.parse(document.getElementById('photos_dict').textContent);
    const bucket_url = JSON.parse(document.getElementById('bucket_url').textContent);
    const lead_images = photos_dict[leadId];

    const imagesSlider = document.getElementsByClassName('slick-track')[0];
    console.log(imagesSlider);

    imagesModalContainer.style.display = "";
    
    lead_images.forEach(image => {
      const containerDiv = document.createElement('div');
      const imgElement = document.createElement('img');

      imgElement.src = bucket_url + image;

      containerDiv.appendChild(imgElement);
      imagesSlider.appendChild(containerDiv);
    });
  });
});

const closeModal = document.getElementById('closeModal');

closeModal.addEventListener("click", e => imagesModalContainer.style.display = "none");

const sliderPrevious = document.getElementById('sliderPrevious');
const sliderNext = document.getElementById('sliderNext');

sliderPrevious.addEventListener("click", () => $('#imagesSlider').slick('slickNext'));
sliderPrevious.addEventListener("click", () => $('#imagesSlider').slick('slickPrev'));