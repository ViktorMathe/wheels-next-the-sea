document.addEventListener("DOMContentLoaded", function () {
    const addFolderButton = document.getElementById("add-sign");
    const createFolderModal = document.querySelector("#create-folder");
    const closeFolderModal = document.querySelector(".folder-modal .close")
    const allFolders = document.querySelectorAll(".gallery-folder");
    const modal = document.querySelector(".gallery-modal");
    const closeModal = document.querySelector(".gallery-modal .close");
    const mainImage = document.getElementById("main-image");
    const thumbnailRow = document.getElementById("thumbnail-row");
    const prevBtn = document.querySelector(".prev");
    const nextBtn = document.querySelector(".next");
    const addImageButton = document.querySelector("#add-image-button");
    const addImageModal = document.querySelector("#add-image-modal");
    const closeaddImageModal = document.querySelector("#add-image-modal .close");
    const menuToggle = document.querySelector(".menu-toggle");
    const navList = document.querySelector(".nav-list");
    const dropdowns = document.querySelectorAll(".dropdown");

    let eventDropdown = document.getElementById("events-dropdown");
    let currentIndex = 0;
    let currentImages = [];

    let addImageFunction = function () {
        thumbnailRow.appendChild(addImageButton)
        addImageButton.addEventListener("click", function () {
            modal.style.display = "None";
            mainImage.src = "";
            thumbnailRow.innerHTML = "";
            addImageModal.style.display = "flex";
            closeaddImageModal.addEventListener("click", function () {
                addImageModal.style.display = "None";
            })
        })
    }

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

    if (addFolderButton) {
        addFolderButton.addEventListener("click", function () {
            createFolderModal.style.display = "flex";
            closeFolderModal.addEventListener("click", function () {
                createFolderModal.style.display = "None";
            })
        })
    }


    allFolders.forEach(folder => {
        folder.addEventListener("click", function () {
            const folderName = this.getAttribute("data-name");
            const images = Array.from(this.querySelectorAll("img.img-src")).map(img => img.src);

            if (images.length === 0) {
                if (addImageButton) {
                    addImageFunction()
                } else {
                    alert('No images available in this folder!');
                    return
                }
            }

            currentImages = images;
            currentIndex = 0;

            // Fill thumbnails
            thumbnailRow.innerHTML = "";
            if (addImageButton) {
                addImageFunction();
            }
            images.forEach((src, idx) => {
                const thumb = document.createElement("img");
                thumb.src = src;
                thumb.addEventListener("click", () => {
                    currentIndex = idx;
                    updateMainImage();
                });
                thumbnailRow.appendChild(thumb);
            });

            // Show modal and first image
            modal.style.display = "flex";
            updateMainImage();
        });
    });

    function updateMainImage() {
        mainImage.src = currentImages[currentIndex];
    }

    closeModal.addEventListener("click", () => {
        modal.style.display = "none";
        mainImage.src = "";
        thumbnailRow.innerHTML = "";
    });

    modal.addEventListener("click", (e) => {
        if (e.target === modal) {
            modal.style.display = "none";
            mainImage.src = "";
            thumbnailRow.innerHTML = "";
        }
    });

    prevBtn.addEventListener("click", () => {
        currentIndex = (currentIndex - 1 + currentImages.length) % currentImages.length;
        updateMainImage();
    });

    nextBtn.addEventListener("click", () => {
        currentIndex = (currentIndex + 1) % currentImages.length;
        updateMainImage();
    });
});