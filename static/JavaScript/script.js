// =========================================================================
// 1. DOM Content Loaded Event
// =========================================================================
document.addEventListener('DOMContentLoaded', function () {
    // Initialize the calendar on the page
    new Calendar({
        id: '#color-calendar',
        theme: 'basic',
        primaryColor: '#1a237e',
        weekdayType: 'short',
        monthDisplayType: 'long',
        calendarSize: 'large',
        layoutModifiers: ['month-left-align'],
        eventsData: []
    });
});

// =========================================================================
// 2. Clock Functionality
// =========================================================================
var clockElement = document.getElementById('clock');

// Function to update the clock display
function updateClock() {
    clockElement.textContent = new Date().toLocaleTimeString(); // Format the time
}

// Update the clock every second
setInterval(updateClock, 1000);

// =========================================================================
// 3. Modal Functionality
// =========================================================================
var modal = document.getElementById("edit-modal");
var btn = document.getElementById("add-student-btn");
var overlay = document.getElementById("overlay");

// Function to show the modal
function showModal() {
    modal.style.display = "block"; // Show the modal
}

// Function to hide the modal
function hideModal() {
    modal.style.display = "none"; // Hide the modal
}

// Open the modal when the button is clicked
btn.onclick = showModal;

// Close the modal when the user clicks anywhere outside of it
window.onclick = function (event) {
    if (event.target === modal) {
        hideModal();
    }
};

// Get all close buttons
var closeButtons = document.querySelectorAll(".close");

// Add click event to each button
closeButtons.forEach(function (btn) {
    btn.addEventListener("click", function () {
        // Find the parent modal to close
        var modal = this.closest(".modal");
        if (modal) {
            modal.style.display = "none";
        }
    });
});

// =========================================================================
// 4. Form Submission Handling
// =========================================================================
var form = document.querySelector("form");

// Handle form submission
form.addEventListener("submit", function (event) {
    const formData = new FormData(form); // Create a FormData object
    fetch(form.action, {
        method: 'POST',
        body: formData,
    });
    hideModal();
});

// Show overlay if it exists
document.addEventListener("DOMContentLoaded", function () {
    if (overlay) {
        overlay.style.display = "block";  // Show the modal
    }
});