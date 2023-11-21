// Get references to the modal elements
const modalOverlay = document.getElementById("modalOverlay");
// const closeModalButton = document.getElementById("closeModal");

// Set the scroll percentage
const scrollPercentageThreshold = 50;

// Function to show the modal
function showModal() {
  modalOverlay.style.display = "flex";
}

// Function to close the modal
function closeModal() {
  modalOverlay.style.display = "none";
}

// Event listener for the close button
// closeModalButton.addEventListener("click", closeModal);

// Event listener for scrolling
window.addEventListener("scroll", () => {
  const scrollY = window.scrollY || window.pageYOffset;
  const windowHeight = window.innerHeight;
  const totalHeight = document.body.clientHeight;
  const scrolledPercentage = (scrollY / (totalHeight - windowHeight)) * 100;
  console.log(scrolledPercentage);

  if (scrolledPercentage >= scrollPercentageThreshold) {
    showModal();
  }
});
