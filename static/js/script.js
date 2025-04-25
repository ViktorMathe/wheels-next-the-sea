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
    const uploadForm = document.getElementById("upload-form");
    const menuToggle = document.querySelector(".menu-toggle");
    const navList = document.querySelector(".nav-list");
    const dropdowns = document.querySelectorAll(".dropdown");
    const fileInput = document.querySelector("#id_images");
    const previewContainer = document.getElementById("uploaded-file");
    let draggableFileArea = document.querySelector(".drag-file-area");
    let browseFileText = document.querySelector(".browse-files");
    let uploadIcon = document.querySelector(".upload-icon");
    let dragDropText = document.querySelector(".dynamic-message");
    let eventDropdown = document.getElementById("events-dropdown");
    let cannotUploadMessage = document.querySelector(".cannot-upload-message");
    let cancelAlertButton = document.querySelector(".cancel-alert-button");
    let uploadedFile = document.querySelector(".file-block");
    let fileName = document.querySelector(".file-name");
    let fileSize = document.querySelector(".file-size");
    let progressBar = document.querySelector(".progress-bar");
    let removeFileButton = document.querySelector(".remove-file-icon");
    let uploadButton = document.querySelector(".upload-button");
    let fileFlag = 0;
    let currentIndex = 0;
    let currentImages = [];
    let selectedFiles = [];


    function getCSRFToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            .split('=')[1];

        return cookieValue;
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
            targetFolder = this.getAttribute("data-name");
            if(addImageButton){
            document.getElementById("id_folder").value = targetFolder;
            }
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

    let addImageFunction = function () {
        if (!thumbnailRow.contains(addImageButton)) {
            thumbnailRow.appendChild(addImageButton);
        }
        addImageButton.onclick = function () {
            modal.style.display = "None";
            mainImage.src = "";
            thumbnailRow.innerHTML = "";
            addImageModal.style.display = "flex";
            closeaddImageModal.addEventListener("click", function () {
                addImageModal.style.display = "None";
                uploadForm.reset();
                uploadedFile.style.display = "none";
                fileInput.value = '';
                uploadIcon.innerHTML = 'file_upload';
                dragDropText.innerHTML = 'Drag & drop any file here';
            })
        }
    }

    var isAdvancedUpload = function () {
        var div = document.createElement('div');
        return (('draggable' in div) || ('ondragstart' in div && 'ondrop' in div)) && 'FormData' in window && 'FileReader' in window;
    }();


    if (fileInput) {
        fileInput.addEventListener("click", () => {
            fileInput.value = '';
        });

        fileInput.addEventListener("change", e => {
            const newFiles = Array.from(e.target.files);
        
            // Append new files without duplicates (by name + size)
            newFiles.forEach(newFile => {
                const exists = selectedFiles.some(existingFile => 
                    existingFile.name === newFile.name && existingFile.size === newFile.size
                );
                if (!exists) selectedFiles.push(newFile);
            });
        
            updatePreview();
            fileInput.value = ''; // Reset input so same file can be re-added
        });

    }
    if (uploadButton) {
        uploadButton.addEventListener("click", () => {
            let isFileUploaded = fileInput.value;
            if (isFileUploaded != '') {
                if (fileFlag == 0) {
                    fileFlag = 1;
                    var width = 0;
                    var id = setInterval(frame, 50);
                    function frame() {
                        if (width >= 390) {
                            clearInterval(id);
                            uploadButton.innerHTML = `<span class="material-icons-outlined upload-button-icon"> check_circle </span> Uploaded`;
                        } else {
                            width += 5;
                            progressBar.style.width = width + "px";
                        }
                    }
                }
            } else {
                cannotUploadMessage.style.cssText = "display: flex; animation: fadeIn linear 1.5s;";
            }
        });
    } 
    if (cancelAlertButton) {
        cancelAlertButton.addEventListener("click", () => {
            cannotUploadMessage.style.cssText = "display: none;";
        });
    }

    if (isAdvancedUpload) {
        if (draggableFileArea) {
            ["drag", "dragstart", "dragend", "dragover", "dragenter", "dragleave", "drop"].forEach(evt =>
                draggableFileArea.addEventListener(evt, e => {
                    e.preventDefault();
                    e.stopPropagation();
                })
            );

            ["dragover", "dragenter"].forEach(evt => {
                draggableFileArea.addEventListener(evt, e => {
                    e.preventDefault();
                    e.stopPropagation();
                    uploadIcon.innerHTML = 'file_download';
                    dragDropText.innerHTML = 'Drop your file here!';
                });
            });

            draggableFileArea.addEventListener("drop", e => {
                uploadIcon.innerHTML = 'check_circle';
                dragDropText.innerHTML = 'File Dropped Successfully!';
                document.querySelector(".label").innerHTML = `drag & drop or <span class="browse-files"> <input type="file" class="default-file-input"/> <span class="browse-files-text"> browse file</span></span>`;
            
                const droppedFiles = Array.from(e.dataTransfer.files);
                droppedFiles.forEach(file => {
                    const exists = selectedFiles.some(existingFile => 
                        existingFile.name === file.name && existingFile.size === file.size
                    );
                    if (!exists) selectedFiles.push(file);
                });
            
                updatePreview();
            });
        }
    }

    if (removeFileButton) {
        removeFileButton.addEventListener("click", () => {
            uploadedFile.style.cssText = "display: none;";
            fileInput.value = '';
            uploadIcon.innerHTML = 'file_upload';
            dragDropText.innerHTML = 'Drag & drop any file here';
            document.querySelector(".label").innerHTML = `or <span class="browse-files"> <input type="file" class="default-file-input"/> <span class="browse-files-text">browse file</span> <span>from device</span> </span>`;
            uploadButton.innerHTML = "Upload";
        });
    }

    if (uploadForm) {
        uploadForm.addEventListener("submit", function (e) {
            e.preventDefault();

            if (selectedFiles.length === 0) {
                alert("Please select at least one image to upload.");
                return;
            }

            const formData = new FormData(uploadForm);
            formData.delete("images"); // Remove original file list
            selectedFiles.forEach(file => {
                formData.append("images", file);
            });

            const xhr = new XMLHttpRequest();
            xhr.upload.addEventListener("progress", function (e) {
                if (e.lengthComputable) {
                    const percent = (e.loaded / e.total) * 100;
                    progressBar.style.display = "block";
                    progressBar.value = percent;
                }
            });

            xhr.addEventListener("load", function () {
                if (xhr.status === 200) {
                    progressBar.value = 100;
                    setTimeout(() => {
                        progressBar.style.display = "none";
                        previewContainer.innerHTML = "";
                        addImageModal.style.display = "none";
                        selectedFiles = [];
                        window.location.reload();
                    }, 800);
                } else {
                    alert("Upload failed.");
                    console.error(xhr.responseText);
                }
            });

            xhr.open("POST", uploadForm.action);
            xhr.setRequestHeader("X-CSRFToken", getCSRFToken());
            xhr.send(formData);
        });
    }

    function updatePreview() {
        uploadedFile.innerHTML = ""; // Clear previous previews
    
        if (selectedFiles.length === 0) {
            uploadedFile.innerHTML = "<p>No files selected.</p>";
            return;
        }
    
        selectedFiles.forEach((file, index) => {
            const fileBlock = document.createElement("div");
            fileBlock.className = "file-preview";
    
            if (file.type.startsWith("image/")) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const img = document.createElement("img");
                    img.src = e.target.result;
                    img.alt = file.name;
                    img.classList.add("preview-image");
                    fileBlock.appendChild(img);
                };
                reader.readAsDataURL(file);
                uploadedFile.style.display = 'flex';
            } else {
                const text = document.createElement("p");
                text.textContent = file.name;
                fileBlock.appendChild(text);
            }
    
            const removeBtn = document.createElement("button");
            removeBtn.className = "remove-file-icon";
            removeBtn.innerHTML = "×";
            removeBtn.title = "Remove";
            removeBtn.onclick = () => {
                selectedFiles.splice(index, 1);
                updatePreview();
            };
    
            fileBlock.appendChild(removeBtn);
            uploadedFile.appendChild(fileBlock);
        });
    
        fileFlag = 0;
        progressBar.style.width = 0;
        uploadButton.innerHTML = "Upload";
    }

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