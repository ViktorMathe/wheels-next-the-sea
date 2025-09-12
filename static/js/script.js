document.addEventListener("DOMContentLoaded", function () {
    const addFolderButton = document.getElementById("add-sign");
    const createFolderModal = document.querySelector("#create-folder");
    const closeFolderModal = document.querySelector(".folder-modal .close");
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
    const previewContainer = document.getElementById("uploaded-file");
    let fileInput = document.querySelector("#id_images");
    const progressBar = document.getElementById("progressBar");
    const uploadButton = document.querySelector(".upload-button");
    let draggableFileArea = document.querySelector(".drag-file-area");
    let uploadIcon = document.querySelector(".upload-icon");
    let dragDropText = document.querySelector(".dynamic-message");
    let eventDropdown = document.getElementById("events-dropdown");
    let cannotUploadMessage = document.querySelector(".cannot-upload-message");
    let cancelAlertButton = document.querySelector(".cancel-alert-button");
    let uploadedFile = document.querySelector(".file-block");
    let fileFlag = 0;
    let currentIndex = 0;
    let currentImages = [];
    let selectedFiles = [];
    const aboutModal = document.getElementById("aboutUsModal");
    const openBtn = document.getElementById("openModalBtn");
    const closeBtn = document.getElementById("closeModalBtn");

    // --- About modal ---
    if (openBtn) openBtn.addEventListener("click", () => (aboutModal.style.display = "block"));
    if (closeBtn) closeBtn.addEventListener("click", () => (aboutModal.style.display = "none"));
    window.addEventListener("click", e => { if (e.target === aboutModal) aboutModal.style.display = "none"; });

    // --- Loading overlay ---
    function showOverlay(message = "Please wait...") {
        let overlay = document.getElementById("loading-overlay");
        if (!overlay) {
            overlay = document.createElement("div");
            overlay.id = "loading-overlay";
            overlay.style.cssText = `
                position: fixed; top:0; left:0; width:100%; height:100%;
                background: rgba(0,0,0,0.5); display:flex; align-items:center;
                justify-content:center; z-index:9999; flex-direction: column;
                color: #fff; font-size: 1.5rem; backdrop-filter: blur(3px);
            `;
            overlay.innerHTML = `
                <div class="spinner" style="
                    border: 4px solid #fff3;
                    border-top: 4px solid #fff;
                    border-radius: 50%;
                    width: 50px; height:50px;
                    animation: spin 1s linear infinite;
                    margin-bottom: 20px;
                "></div>
                <div class="overlay-message">${message}</div>
            `;
            document.body.appendChild(overlay);
            const style = document.createElement("style");
            style.innerHTML = `@keyframes spin {0% { transform: rotate(0deg);} 100% { transform: rotate(360deg);} }`;
            document.head.appendChild(style);
        } else overlay.querySelector(".overlay-message").textContent = message;
        overlay.style.display = "flex";
    }
    function hideOverlay() { const overlay = document.getElementById("loading-overlay"); if (overlay) overlay.style.display = "none"; }

    // --- CSRF ---
    function getCSRFToken() {
        return document.cookie.split("; ").find(row => row.startsWith("csrftoken=")).split("=")[1];
    }

    // --- Navigation ---
    menuToggle.addEventListener("click", () => navList.classList.toggle("active"));
    eventDropdown.addEventListener("click", () => eventDropdown.classList.toggle("active"));
    navList.addEventListener("click", e => { if (!e.target.closest(".dropdown")) closeAllDropdowns(); });
    document.addEventListener("click", e => {
        if (!e.target.closest(".nav-list") && !e.target.closest(".menu-toggle")) {
            navList.classList.remove("active");
            closeAllDropdowns();
        }
    });
    function closeAllDropdowns() { dropdowns.forEach(d => d.classList.remove("active")); }

    // --- Reviews ---
    document.querySelectorAll(".review-items").forEach(item => {
        const textElement = item.querySelector(".review-text");
        const fullText = textElement.getAttribute("data-full");
        const readMoreBtn = item.querySelector(".read-more");
        if (textElement.scrollHeight <= textElement.clientHeight) readMoreBtn.style.display = "none";
        readMoreBtn.addEventListener("click", () => {
            textElement.textContent = fullText;
            textElement.style.display = "block";
            textElement.style.overflow = "visible";
            textElement.style.webkitLineClamp = "unset";
            readMoreBtn.remove();
        });
    });

    document.querySelectorAll(".remove-file-icon").forEach(btn => {
        btn.addEventListener("click", async (e) => {
            e.stopPropagation();
            showOverlay("Deleting image...");
            const image_url = btn.dataset.url; // Use a data attribute
            try {
                const res = await fetch("/delete-image/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCSRFToken()
                    },
                    body: JSON.stringify({ image_url })
                });
                const result = await res.json();
                if (result.success) window.location.reload();
                else {
                    alert(result.error || "Failed to delete");
                    hideOverlay();
                }
            } catch (err) {
                console.error(err);
                hideOverlay();
            }
        });
    });

    // --- Folder modal ---
    if (addFolderButton) addFolderButton.addEventListener("click", () => {
        createFolderModal.style.display = "flex";
        closeFolderModal.addEventListener("click", () => createFolderModal.style.display = "none");
    });

    // --- Gallery / Year_gallery modal ---
    allFolders.forEach(folder => {
        folder.addEventListener("click", event => {
            const targetFolder = folder.getAttribute("data-name");
            if (addImageButton) document.getElementById("id_folder").value = targetFolder;

            const imageElements = Array.from(folder.querySelectorAll("img.img-src"));
            const images = imageElements.map(img => img.src);

            if (images.length === 0) { if (addImageButton) addImageFunction(); else { alert("No images available!"); return; } }

            let clickedIndex = 0;
            if (event.target.tagName === "IMG" && event.target.classList.contains("img-src")) {
                clickedIndex = images.indexOf(event.target.src);
            }

            currentImages = images;
            currentIndex = clickedIndex;
            thumbnailRow.innerHTML = "";
            if (addImageButton) addImageFunction();

            images.forEach((src, idx) => {
                const thumbWrapper = document.createElement("div");
                thumbWrapper.classList.add("thumbnail-wrapper");

                const thumb = document.createElement("img");
                thumb.src = src;
                thumb.classList.add("thumbnail");
                if (idx === currentIndex) thumb.classList.add("active");
                thumb.addEventListener("click", () => { currentIndex = idx; updateMainImage(); updateThumbnailHighlight(); });
                thumbWrapper.appendChild(thumb);

                // --- Remove button with dynamic deletion ---
                if (addImageButton) {
                    const removeBtn = document.createElement("button");
                    removeBtn.textContent = "✕";
                    removeBtn.classList.add("remove-file-icon");
                    removeBtn.addEventListener("click", async e => {
                        e.stopPropagation();
                        if (!confirm("Delete this image?")) return;
                        showOverlay("Deleting image...");
                        try {
                            const res = await fetch("/gallery/delete-image/", {
                                method: "POST",
                                headers: { "Content-Type": "application/json", "X-CSRFToken": getCSRFToken() },
                                body: JSON.stringify({ image_url: new URL(src).href })
                            });
                            const result = await res.json();
                            if (result.success) {
                                currentImages.splice(idx, 1);
                                thumbWrapper.remove();
                                if (currentImages.length === 0) mainImage.src = "";
                                else {
                                    if (currentIndex >= currentImages.length) currentIndex = currentImages.length - 1;
                                    updateMainImage();
                                }
                            } else alert(result.error || "Failed to delete");
                        } catch (err) { console.error(err); alert("Server error"); }
                        finally { hideOverlay(); }
                    });
                    thumbWrapper.appendChild(removeBtn);
                }
                thumbnailRow.appendChild(thumbWrapper);
            });

            modal.style.display = "flex";
            updateMainImage();
        });
    });

    function updateThumbnailHighlight() {
        const allThumbs = thumbnailRow.querySelectorAll("img");
        allThumbs.forEach((t, i) => t.classList.toggle("active", i === currentIndex));
    }

    let addImageFunction = function () {
        if (!thumbnailRow.contains(addImageButton)) thumbnailRow.appendChild(addImageButton);
        addImageButton.onclick = () => {
            modal.style.display = "none";
            mainImage.src = "";
            thumbnailRow.innerHTML = "";
            addImageModal.style.display = "flex";
            closeaddImageModal.addEventListener("click", () => {
                addImageModal.style.display = "none";
                uploadForm.reset();
                uploadedFile.style.display = "none";
                fileInput.value = "";
                uploadIcon.innerHTML = "file_upload";
                dragDropText.innerHTML = "Drag & drop any file here";
            });
        };
    };

    // --- Drag & Drop + Preview ---
    const isAdvancedUpload = (() => { const d = document.createElement("div"); return ("draggable" in d || ("ondragstart" in d && "ondrop" in d)) && "FormData" in window && "FileReader" in window; })();
    if (fileInput) {
        fileInput.addEventListener("click", () => fileInput.value = "");
        fileInput.addEventListener("change", e => {
            Array.from(e.target.files).forEach(f => { if (!selectedFiles.some(sf => sf.name === f.name && sf.size === f.size)) selectedFiles.push(f); });
            updatePreview();
        });
    }
    if (uploadButton) uploadButton.addEventListener("click", () => {
        if (selectedFiles.length === 0) { cannotUploadMessage.style.cssText = "display:flex; animation:fadeIn 1.5s;"; return; }
        uploadForm.requestSubmit();
    });
    if (cancelAlertButton) cancelAlertButton.addEventListener("click", () => cannotUploadMessage.style.cssText = "display:none;");
    if (isAdvancedUpload && draggableFileArea) {
        ["drag", "dragstart", "dragend", "dragover", "dragenter", "dragleave", "drop"].forEach(evt => draggableFileArea.addEventListener(evt, e => { e.preventDefault(); e.stopPropagation(); }));
        ["dragover", "dragenter"].forEach(evt => draggableFileArea.addEventListener(evt, () => { uploadIcon.innerHTML = "file_download"; dragDropText.innerHTML = "Drop your file here!"; }));
        draggableFileArea.addEventListener("drop", e => {
            uploadIcon.innerHTML = "check_circle";
            dragDropText.innerHTML = "File Dropped Successfully!";
            Array.from(e.dataTransfer.files).forEach(f => { if (!selectedFiles.some(sf => sf.name === f.name && sf.size === f.size)) selectedFiles.push(f); });
            updatePreview();
        });
    }

    // --- Upload ---
    if (uploadForm) {
        uploadForm.addEventListener("submit", async e => {
            e.preventDefault();
            if (selectedFiles.length === 0) { alert("Select at least one image."); return; }
            showOverlay("Uploading images...");
            progressBar.style.display = "block"; progressBar.style.width = "0%";
            try {
                const fd = new FormData(uploadForm);
                fd.delete("images");
                selectedFiles.forEach(f => fd.append("images", f));
                await new Promise((resolve, reject) => {
                    const xhr = new XMLHttpRequest();
                    xhr.open("POST", uploadForm.action);
                    xhr.setRequestHeader("X-CSRFToken", getCSRFToken());
                    xhr.upload.addEventListener("progress", e => { if (e.lengthComputable) progressBar.style.width = ((e.loaded / e.total) * 100) + "%"; });
                    xhr.onload = () => xhr.status === 200 ? resolve() : reject("Upload failed " + xhr.status);
                    xhr.onerror = () => reject("Network error");
                    xhr.send(fd);
                });
                progressBar.style.width = "100%";
                setTimeout(() => window.location.reload(), 700);
            } catch (err) { console.error(err); alert(err); hideOverlay(); }
        });
    }

    function updatePreview() {
        uploadedFile.innerHTML = "";
        if (selectedFiles.length === 0) { uploadedFile.innerHTML = "<p>No files selected.</p>"; return; }
        selectedFiles.forEach((f, i) => {
            const block = document.createElement("div"); block.className = "file-preview";
            if (f.type.startsWith("image/")) {
                const reader = new FileReader();
                reader.onload = e => { const img = document.createElement("img"); img.src = e.target.result; img.alt = f.name; img.classList.add("preview-image"); block.appendChild(img); };
                reader.readAsDataURL(f); uploadedFile.style.display = 'flex';
            } else { const t = document.createElement("p"); t.textContent = f.name; block.appendChild(t); }
            const removeBtn = document.createElement("button"); removeBtn.className = "remove-file-icon"; removeBtn.innerHTML = "×"; removeBtn.title = "Remove";
            removeBtn.onclick = () => { selectedFiles.splice(i, 1); updatePreview(); };
            block.appendChild(removeBtn);
            uploadedFile.appendChild(block);
        });
        fileFlag = 0; progressBar.style.width = 0; uploadButton.innerHTML = "Upload";
    }

    function rebindFileInput() {
        const newInput = document.querySelector(".default-file-input"); fileInput = newInput;
        if (fileInput) {
            fileInput.addEventListener("click", () => fileInput.value = "");
            fileInput.addEventListener("change", e => {
                Array.from(e.target.files).forEach(f => { if (!selectedFiles.some(sf => sf.name === f.name && sf.size === f.size)) selectedFiles.push(f); });
                updatePreview(); fileInput.value = "";
            });
        }
    }

    document.querySelectorAll('.delete-image-btn').forEach((btn) => {
        btn.addEventListener('click', function () {
            const url = this.dataset.url
            if (!confirm('Delete this image?')) return

            showOverlay('Deleting image...')
            fetch('/gallery/delete_image/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({ image_url: url })
            })
                .then((r) => r.json())
                .then((data) => {
                    hideOverlay()
                    if (data.success) location.reload()
                    else alert('Error: ' + data.error)
                })
        })
    })

    // MULTI DELETE
    const deleteSelectedBtn = document.getElementById('delete-selected')
    if (deleteSelectedBtn) {
        deleteSelectedBtn.addEventListener('click', function () {
            const selected = [...document.querySelectorAll('.select-image:checked')].map((c) => c.dataset.url)
            if (!selected.length) {
                alert('No images selected')
                return
            }
            if (!confirm('Delete selected images?')) return

            showOverlay('Deleting selected images...')
            fetch('./delete_multiple_images/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({ urls: selected })
            })
                .then((r) => r.json())
                .then((data) => {
                    hideOverlay()
                    if (data.success) location.reload()
                    else alert('Error: ' + data.error)
                })
        })
    }

    function updateMainImage() { if (currentImages.length > 0) mainImage.src = currentImages[currentIndex]; updateThumbnailHighlight(); }

    if (modal) {
        closeModal.addEventListener("click", () => { modal.style.display = "none"; mainImage.src = ""; thumbnailRow.innerHTML = ""; });
        modal.addEventListener("click", e => { if (e.target === modal) { modal.style.display = "none"; mainImage.src = ""; thumbnailRow.innerHTML = ""; } });
    }

    if (prevBtn) prevBtn.addEventListener("click", () => { currentIndex = (currentIndex - 1 + currentImages.length) % currentImages.length; updateMainImage(); });
    if (nextBtn) nextBtn.addEventListener("click", () => { currentIndex = (currentIndex + 1) % currentImages.length; updateMainImage(); });
});