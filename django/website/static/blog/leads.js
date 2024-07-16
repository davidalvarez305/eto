const pageElements = document.querySelectorAll(".paginationChevron");

pageElements.forEach(chevron => {
  chevron.addEventListener('click', event => {
    const chevronType = chevron.getAttribute('data-chevron-value');
    const maxPages = JSON.parse(document.getElementById('max-pages').textContent);

    const options = {
      left_chevron: -1,
      right_chevron: 1
    }

    if (!chevronType) return;

    const currentPage = parseInt(new URLSearchParams(window.location.search).get('page')) || 1;

    // handle left chevron & value of 1:
    if (chevronType === "left_chevron" && currentPage === 1) return;

    // handle right chevron & max value:
    if (chevronType === "right_chevron" && currentPage === maxPages) return;

    const qs = new URLSearchParams(window.location.search);
    qs.set('page', currentPage + options[chevronType]);

    const url = buildURL();
    url.search = qs.toString();

    window.location.replace(url.href);
  });
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

function buildURL() {
  const { origin, pathname } = window.location;

  return new URL(origin + pathname);
}