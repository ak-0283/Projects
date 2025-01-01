document.addEventListener("DOMContentLoaded", () => {
    const deleteButtons = document.querySelectorAll("form[action*='DELETE'] button");
  
    deleteButtons.forEach(button => {
      button.addEventListener("click", (event) => {
        const confirmation = confirm("Are you sure you want to delete this chat?");
        if (!confirmation) {
          event.preventDefault(); // Prevents the form from submitting if user clicks 'Cancel'
        }
      });
    });
  });


// Functionality for Scroll to Top Button
window.onscroll = function () {
  const scrollTopBtn = document.getElementById("scrollTopBtn");

  // Show the button when the user scrolls down
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    scrollTopBtn.style.display = "block";
  } else {
    scrollTopBtn.style.display = "none";
  }
};

// Smooth scroll to top function
function scrollToTop() {
  window.scrollTo({ top: 0, behavior: "smooth" });
}

// Add event listener to the button
document.getElementById("scrollTopBtn").addEventListener("click", scrollToTop);
