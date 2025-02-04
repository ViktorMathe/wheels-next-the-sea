document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.querySelector(".menu-toggle");
    const navList = document.querySelector(".nav-list");
    const dropdowns = document.querySelectorAll(".dropdown");
    // Toggle main mobile menu
    menuToggle.addEventListener("click", function () {
        navList.classList.toggle("active");
    });
    // Toggle dropdown menus inside mobile menu
    dropdowns.forEach(dropdown => {
        dropdown.addEventListener("click", function (event) {
            event.stopPropagation(); // Prevent event bubbling
            this.classList.toggle("active");
        });
    });
 });