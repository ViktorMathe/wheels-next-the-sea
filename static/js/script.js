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
    eventDropdown.addEventListener("click", function (event) {
        if (eventDropdown.classList.contains("active")) {
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

    document.querySelectorAll(".review-items").forEach(function (item) {
        let textElement = item.querySelector(".review-text");
        let fullText = textElement.getAttribute("data-full");
        let readMoreBtn = item.querySelector(".read-more");

        // Hide "Read More" if content is already short
        if (textElement.scrollHeight <= textElement.clientHeight) {
            readMoreBtn.style.display = "none";
        }

        readMoreBtn.addEventListener("click", function () {
            textElement.textContent = fullText; // Replace with full text
            textElement.style.display = "block";
            textElement.style.overflow = "visible";
            textElement.style.webkitLineClamp = "unset"; // Remove line clamp
            readMoreBtn.remove(); // Remove button after expanding
        });
    });


   /*  const yearBoxes = document.querySelectorAll(".gallery-folder");
    const modal = document.querySelector(".gallery-modal");
    const modalImage = document.querySelector(".main-image");
    const thumbnailsContainer = document.querySelector(".gallery-thumbnails");
    const prevButton = document.querySelector(".prev");
    const nextButton = document.querySelector(".next");
    const closeModal = document.querySelector(".gallery-modal .close");
    const allImages = document.querySelector(".img-src")

    let images = [];
    let currentIndex = 0;

    // Open modal and show images
    yearBoxes.forEach(box => {
        box.addEventListener("click", function () {
            const folderName = this.getAttribute("data-name");
            const myGallery = cloudinary.galleryWidget({ 
                container: "#my-gallery", 
                cloudName: "vikmath1119", 
                mediaAssets: [{ tag: folderName }]    // by default mediaType: "image"
              });
        
            /* const folderImagesLength = this.childNodes[3].getElementsByClassName('img-src').length
            thumbnailsContainer.innerHTML = ""; // Clear previous thumbnails
            images = []; // Reset images array
            console.log(document.getElementsByClassName('modalrc'))
            // Load full gallery for the selected year
            for (let i = 1; i <= folderImagesLength; i++) {
                let imgSrc = document.getElementsByClassName('modalrc')
                images.push(imgSrc);

                let thumbImg = document.createElement("img");
                thumbImg.src = imgSrc;
                thumbImg.alt = `Event ${folderName}`;
                thumbImg.dataset.index = i - 1;

                // Clicking a thumbnail changes the main image
                thumbImg.addEventListener("click", function () {
                    currentIndex = parseInt(this.dataset.index);
                    updateMainImage();
                });

                thumbnailsContainer.appendChild(thumbImg);
            }

            currentIndex = 0;
            updateMainImage(); */
           /*  modal.style.display = "flex";
        });
    });

   /*  // Function to update the main image
    function updateMainImage() {
        modalImage.src = images[currentIndex];
    }

    // Navigation Buttons
    prevButton.addEventListener("click", function () {
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        updateMainImage();
    });

    nextButton.addEventListener("click", function () {
        currentIndex = (currentIndex + 1) % images.length;
        updateMainImage();
    }); 

    // Close Modal
    closeModal.addEventListener("click", function () {
        modal.style.display = "none";
    });

    modal.addEventListener("click", function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    }); */ 
});