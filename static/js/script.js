document.addEventListener("DOMContentLoaded", function () {
  // === NAVBAR ===
  const menuToggle = document.querySelector(".menu-toggle");
  const navList = document.querySelector(".nav-list");
  const eventsDropdown = document.getElementById("events-dropdown");
  const dropdownMenu = eventsDropdown.querySelector(".dropdown-menu");
  const editAboutUs = document.getElementById("openModalBtn");


  var password1 = document.getElementById("id_password1");
  var password2 = document.getElementById("id_password2");
  var passwordRequirements = document.getElementById("password-requirements");
  var passwordMismatch = document.getElementById("password-mismatch");
  var passwordMatch = document.getElementById("password-match");
  var submitButton = document.getElementById("submit_button");

  function checkAvailability(input, url, feedbackElement) {
    fetch(`${url}?${new URLSearchParams({ [input.name]: input.value })}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok.');
        }
        return response.json();
      })
      .then(data => {
        if (data.error) {
          feedbackElement.textContent = `Error: ${data.error}`;
          feedbackElement.style.color = 'red';
        } else if (data.exists) {
          feedbackElement.textContent = `${input.name.replace(/^\w/, c => c.toUpperCase())} is already taken.`;
          feedbackElement.style.color = 'red';
        } else {
          feedbackElement.textContent = '';
        }
        validateForm();
      })
      .catch(error => {
        feedbackElement.textContent = 'Please fill out this field!';
        feedbackElement.style.color = 'red';
        validateForm();
      });
  }

  function validatePassword() {
    var length = document.getElementById("length");
    var uppercase = document.getElementById("uppercase");
    var numeric = document.getElementById("numeric");
    var special = document.getElementById("special");

    var isValid = true;

    // Check the length
    if (password1.value.length >= 8) {
      length.classList.remove("invalid");
      length.classList.add("valid");
    } else {
      length.classList.remove("valid");
      length.classList.add("invalid");
      isValid = false;
    }

    // Check for uppercase letter
    if (/[A-Z]/.test(password1.value)) {
      uppercase.classList.remove("invalid");
      uppercase.classList.add("valid");
    } else {
      uppercase.classList.remove("valid");
      uppercase.classList.add("invalid");
      isValid = false;
    }

    // Check for numeric character
    if (/[0-9]/.test(password1.value)) {
      numeric.classList.remove("invalid");
      numeric.classList.add("valid");
    } else {
      numeric.classList.remove("valid");
      numeric.classList.add("invalid");
      isValid = false;
    }

    // Check for special character
    if (/[\W_]/.test(password1.value)) {
      special.classList.remove("invalid");
      special.classList.add("valid");
    } else {
      special.classList.remove("valid");
      special.classList.add("invalid");
      isValid = false;
    }

    // Show or hide password requirements
    passwordRequirements.style.display = "block";
    if (length.classList.contains("valid") && uppercase.classList.contains("valid") &&
      numeric.classList.contains("valid") && special.classList.contains("valid")) {
      passwordRequirements.style.display = "block";
    }

    if (password1.value !== password2.value) {
      passwordMatch.style.display = "block";
      passwordMatch.classList.remove('valid'); // Remove the 'valid' class
      passwordMatch.classList.add('invalid'); // Add the 'invalid' class
      passwordMatch.textContent = 'Passwords do not match'; // Set the text content
      isValid = false;
    } else {
      passwordMatch.style.display = "block";
      passwordMatch.classList.remove('invalid'); // Remove the 'invalid' class
      passwordMatch.classList.add('valid'); // Add the 'valid' class
      passwordMatch.textContent = 'Password is matching! :)'; // Set the text content
    }

    return isValid;
  }


  function validateForm() {
    var isPasswordValid = validatePassword();

    submitButton.disabled = !(isPasswordValid);
  }


  if (password1 && password2) {
    password1.addEventListener('input', validatePassword);
    password2.addEventListener('input', validatePassword);
  }

  function togglePasswordVisibility(targetId) {
    var passwordField = document.getElementById(targetId);
    var type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordField.setAttribute('type', type);

    var eyeIcon = document.querySelector(`.toggle-password[data-target="${targetId}"] i`);
    eyeIcon.className = type === 'password' ? 'fa fa-eye-slash' : 'fa fa-eye';
  }

  document.querySelectorAll('.toggle-password').forEach(function (toggleElement) {
    toggleElement.addEventListener('click', function () {
      var targetId = this.getAttribute('data-target');
      togglePasswordVisibility(targetId);
    });
  });

  // Remove .remove-bg class when index page loads
  var elementsWithRemoveBg = document.querySelectorAll('.remove-bg');

  // Loop through each element and remove the class
  elementsWithRemoveBg.forEach(function (element) {
    element.classList.remove('remove-bg');
  });

  // Mobile menu toggle
  menuToggle.addEventListener("click", (e) => {
    navList.classList.toggle("active");
  });

  // Events dropdown toggle
  eventsDropdown.querySelector("a").addEventListener("click", (e) => {
    e.preventDefault();
    e.stopPropagation(); // prevent the menu click from interfering
    dropdownMenu.classList.toggle("active");
  });

  // Close dropdown if clicked outside
  document.addEventListener("click", (e) => {
    if (!eventsDropdown.contains(e.target)) {
      dropdownMenu.classList.remove("active");
    }
  });

  if (editAboutUs) {
    editAboutUs.addEventListener("click", () => {
      const aboutUsModal = document.getElementById("aboutUsModal");
      const close = document.querySelector(".close-btn");
      if (aboutUsModal) {
        aboutUsModal.style.display = "block";
      };
      if (close) {
        close.addEventListener("click", () => {
          aboutUsModal.style.display = "none";
        });
      };
    });
  }

  const editBtn = document.getElementById("edit-contact-btn");
  const cancelBtn = document.getElementById("cancel-edit-btn");
  const editDiv = document.getElementById("contact-edit-modal");

  if (editBtn) {
    editBtn.addEventListener("click", () => {
      const close = document.querySelector(".close-btn");
      editDiv.style.display = "block";

      if (close) {
        close.addEventListener("click", () => {
          editDiv.style.display = "none";
        });
      };
    })


    if (cancelBtn) {
      cancelBtn.addEventListener("click", () => {
        editDiv.style.display = "none";
      });

    }
  }

  // === OVERLAY ===
  const overlay = document.getElementById("overlay");
  const progressText = document.getElementById("progress-text");

  function showOverlay(msg) {
    if (overlay) {
      overlay.classList.remove("hidden");
      if (progressText) progressText.textContent = msg || "Processing...";
    }
  }
  function hideOverlay() {
    if (overlay) overlay.classList.add("hidden");
  }

  // === CSRF ===
  function getCSRFToken() {
    return document.cookie
      .split("; ")
      .find((r) => r.startsWith("csrftoken="))
      ?.split("=")[1];
  }

  // === WRITE REVIEW MODAL === //
  const writeReViewBtn = document.getElementById("write-review");
  const reviewFormModal = document.getElementById("review-form-modal");
  if (writeReViewBtn) {
    const close = reviewFormModal.querySelector(".close-btn");
    writeReViewBtn.addEventListener('click', () => {
      reviewFormModal.style.display = "block";
    });
    if (close) {
      close.addEventListener("click", () => (reviewFormModal.style.display = "none"))
    }
  }

  const galleryModal = document.querySelector(".gallery-modal");
  if (!galleryModal) return;
  // === ADD FOLDER MODAL (gallery.html) ===
  const addFolderBtn = document.getElementById("add-sign");
  const folderModal = document.getElementById("create-folder");
  const createFolderBackground = document.querySelector('.create-folder-modal');
  if (addFolderBtn && folderModal) {
    const close = folderModal.querySelector(".close-btn");
    addFolderBtn.addEventListener("click", () => {
      folderModal.classList.remove('hidden');
      createFolderBackground.style.display = "block";
      folderModal.style.display = "flex";
    });
    if (close) {
      close.addEventListener("click", () => { (folderModal.style.display = "none"), (createFolderBackground.style.display = "none") })
    };
  }

  // === ADD IMAGE MODAL (year_gallery.html) ===
  const addImageBtn = document.getElementById("add-image-btn");
  const addImageModal = document.getElementById("add-image-modal");
  if (addImageBtn && addImageModal) {
    const close = addImageModal.querySelector(".close-btn");
    addImageBtn.addEventListener("click", () => {
      addImageModal.classList.remove('hidden');
      addImageModal.style.display = "flex";
    });
    if (close)
      close.addEventListener("click", () => (addImageModal.style.display = "none"));
  }

  // === IMAGE UPLOAD PREVIEW & AJAX ===
  const dropArea = document.getElementById("drop-area");
  const fileInput = document.getElementById("image-input");
  const browseBtn = document.getElementById("browse-btn");
  const previewContainer = document.getElementById("preview-container");
  const uploadForm = document.getElementById("image-upload-form");

  if (dropArea && fileInput && previewContainer && uploadForm) {
    let files = [];

    function updatePreview() {
      previewContainer.innerHTML = "";
      files.forEach((file, index) => {
        const preview = document.createElement("div");
        preview.className = "preview";

        const img = document.createElement("img");
        img.src = URL.createObjectURL(file);

        const removeBtn = document.createElement("button");
        removeBtn.textContent = "×";
        removeBtn.className = "remove";
        removeBtn.addEventListener("click", () => {
          files.splice(index, 1);
          updatePreview();
        });

        preview.appendChild(img);
        preview.appendChild(removeBtn);
        previewContainer.appendChild(preview);
      });
    }

    browseBtn.addEventListener("click", () => fileInput.click());

    fileInput.addEventListener("change", (e) => {
      files.push(...e.target.files);
      updatePreview();
    });

    dropArea.addEventListener("dragover", (e) => {
      e.preventDefault();
      dropArea.classList.add("dragover");
    });
    dropArea.addEventListener("dragleave", () =>
      dropArea.classList.remove("dragover")
    );
    dropArea.addEventListener("drop", (e) => {
      e.preventDefault();
      dropArea.classList.remove("dragover");
      files.push(...e.dataTransfer.files);
      updatePreview();
    });

    uploadForm.addEventListener("submit", (e) => {
      e.preventDefault();
      if (!files.length) {
        alert("No files selected!");
        return;
      }

      const formData = new FormData(uploadForm);
      files.forEach((file) => formData.append("images", file));

      showOverlay("Uploading...");
      fetch(uploadForm.getAttribute("action") || window.location.pathname, {
        method: "POST",
        headers: { "X-CSRFToken": getCSRFToken() },
        body: formData,
      })
        .then((res) => res.json())
        .then((data) => {
          hideOverlay();
          if (data.success) {
            location.reload();
          } else {
            alert("Error: " + data.error);
          }
        })
        .catch((err) => {
          hideOverlay();
          console.error(err);
        });
    });
  }

  // === DELETE SINGLE IMAGE ===
  document.querySelectorAll(".delete-image-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const url = btn.dataset.url;
      const endpoint = btn.dataset.deleteUrl;
      if (!confirm("Delete this image?")) return;

      showOverlay("Deleting image...");
      fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({ image_url: url }),
      })
        .then((r) => r.json())
        .then((data) => {
          hideOverlay();
          if (data.success) location.reload();
          else alert("Error: " + data.error);
        })
        .catch((err) => {
          hideOverlay();
          console.error(err);
        });
    });
  });

  // === DELETE MULTIPLE IMAGES ===
  const deleteSelectedBtn = document.getElementById("delete-selected");
  if (deleteSelectedBtn) {
    deleteSelectedBtn.addEventListener("click", () => {
      const selected = [
        ...document.querySelectorAll(".select-image:checked"),
      ].map((c) => c.dataset.url);
      const endpoint = deleteSelectedBtn.dataset.deleteUrl;
      if (!selected.length) {
        alert("No images selected");
        return;
      }
      if (!confirm("Delete selected images?")) return;

      showOverlay("Deleting selected images...");
      fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({ images: selected }),
      })
        .then((r) => r.json())
        .then((data) => {
          hideOverlay();
          if (data.success) location.reload();
          else alert("Error: " + data.error);
        })
        .catch((err) => {
          hideOverlay();
          console.error(err);
        });
    });
  }

  // === DELETE FOLDER (gallery) === //
  document.querySelectorAll(".delete-folder").forEach(btn => {
    btn.addEventListener("click", async (e) => {
      e.preventDefault();
      const folderName = btn.dataset.folder;
      if (!confirm(`Delete folder "${folderName}" and all its images?`)) return;
      showOverlay("Deleting selected folder with images...");

      try {
        const res = await fetch("./delete-folder/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
          },
          body: JSON.stringify({ folder_name: folderName })
        });

        const result = await res.json();
        if (result.success) {
          alert(`Folder "${folderName}" deleted`);
          hideOverlay();
          location.reload();
        } else {
          alert(result.error || "Failed to delete folder");
        }
      } catch (err) {
        alert("Server error while deleting folder");
      }
    });
  });

  // === IMAGE MODAL VIEWER (year_gallery) ===
  const modal = document.getElementById("image-modal");
  const modalImg = document.getElementById("modal-img");
  if (modal && modalImg) {
    const images = [...document.querySelectorAll(".images-grid img")];
    let currentIndex = -1;

    function openModal(index) {
      currentIndex = index;
      modalImg.src = images[index].src;
      modal.classList.remove('hidden');
      modal.style.display = "flex";
    }
    function closeModal() {
      modal.style.display = "none";
    }

    images.forEach((img, i) =>
      img.addEventListener("click", () => openModal(i))
    );
    modal.querySelector(".close-btn").onclick = closeModal;
    modal.querySelector(".prev").onclick = () =>
      openModal((currentIndex - 1 + images.length) % images.length);
    modal.querySelector(".next").onclick = () =>
      openModal((currentIndex + 1) % images.length);
  }

  const mainImage = document.getElementById("main-image");
  const thumbnailRow = document.getElementById("thumbnail-row");
  const prevBtn = galleryModal.querySelector(".prev");
  const nextBtn = galleryModal.querySelector(".next");
  const closeBtn = galleryModal.querySelector(".close-btn");
  const addImageButton = document.getElementById("add-image-button");

  let currentImages = [];
  let currentIndex = 0;

  // Open gallery modal when clicking any folder image
  document.querySelectorAll(".gallery-preview").forEach((folder) => {
    folder.addEventListener("click", (e) => {
      e.preventDefault();
      const imageElements = Array.from(folder.querySelectorAll("img.img-src"));
      const images = imageElements.map((img) => img.src);
      if (!images.length) return;

      currentImages = images;
      currentIndex = 0;

      // Highlight clicked image if clicked directly
      if (e.target.tagName === "IMG") {
        currentIndex = images.indexOf(e.target.src);
      }

      thumbnailRow.innerHTML = "";
      images.forEach((src, idx) => {
        const wrapper = document.createElement("div");
        wrapper.classList.add("thumbnail-wrapper");

        const thumb = document.createElement("img");
        thumb.src = src;
        thumb.classList.add("thumbnail");
        if (idx === currentIndex) thumb.classList.add("active");

        thumb.addEventListener("click", () => {
          currentIndex = idx;
          updateMainImage();
          updateThumbnailHighlight();
        });

        wrapper.appendChild(thumb);

        // Delete button if superuser
        if (addImageButton) {
          const removeBtn = document.createElement("button");
          removeBtn.textContent = "✕";
          removeBtn.classList.add("remove-file-icon");
          removeBtn.addEventListener("click", (ev) => {
            ev.stopPropagation();
            if (!confirm("Delete this image?")) return;
            deleteImage(src); // your existing deleteImage function
          });
          wrapper.appendChild(removeBtn);
        }

        thumbnailRow.appendChild(wrapper);
      });

      galleryModal.style.display = "flex";
      updateMainImage();
    });
  });

  function updateMainImage() {
    if (currentImages.length > 0) mainImage.src = currentImages[currentIndex];
    updateThumbnailHighlight();
  }

  function updateThumbnailHighlight() {
    if (thumbnailRow) {
      thumbnailRow.querySelectorAll("img").forEach((t, i) => {
        t.classList.toggle("active", i === currentIndex);
      });
    }
  }

  prevBtn?.addEventListener("click", () => {
    currentIndex = (currentIndex - 1 + currentImages.length) % currentImages.length;
    updateMainImage();
  });

  nextBtn?.addEventListener("click", () => {
    currentIndex = (currentIndex + 1) % currentImages.length;
    updateMainImage();
  });

  closeBtn?.addEventListener("click", () => {
    galleryModal.style.display = "none";
    if (mainImage) {
      mainImage.src = "";
    }
    if (thumbnailRow) {
      thumbnailRow.innerHTML = "";
    }
  });

  // Open add image modal from gallery modal
  addImageButton?.addEventListener("click", () => {
    addImageModal.style.display = "flex";
  });

});