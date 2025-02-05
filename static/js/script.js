document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.querySelector(".menu-toggle");
    const navList = document.querySelector(".nav-list");
    const dropdowns = document.querySelectorAll(".dropdown");
    let eventDropdown = document.getElementById("events-dropdown");
    // Toggle main mobile menu (Right-Aligned)
    menuToggle.addEventListener("click", function () {
        navList.classList.toggle("active");
    });
    // Handle dropdown menu opening/closing
    eventDropdown.addEventListener("click", function(event){
        if(eventDropdown.classList.contains("active")){
            eventDropdown.classList.remove("active");
        } else {
            eventDropdown.classList.add("active");
        }
    });

    // Clicking inside nav-list closes dropdowns but keeps the mobile menu open
    navList.addEventListener("click", function (event) {
        if (!event.target.closest(".dropdown")) {
            closeAllDropdowns(); // Close dropdowns but not the whole menu
        }
    });

    // Close dropdowns and nav-list when clicking outside
    document.addEventListener("click", function (event) {
        if (!event.target.closest(".nav-list") && !event.target.closest(".menu-toggle")) {
            navList.classList.remove("active");
            closeAllDropdowns();
        }
    });
    // Function to close all dropdowns
    function closeAllDropdowns() {
        dropdowns.forEach(dropdown => {
            dropdown.classList.remove("active");
        });
    }
});