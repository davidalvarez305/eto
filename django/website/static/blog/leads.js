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