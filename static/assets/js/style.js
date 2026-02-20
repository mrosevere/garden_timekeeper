// Confirm the JS bundle is loaded
console.log("Garden Timekeeper JS loaded");


// ------------------------------------------------------------
// 1. Auto‑untick "All year" when seasonal months change
//    (This is unrelated to the modal workflow, but kept here
//     because it's part of the task form UX.)
// ------------------------------------------------------------
document.addEventListener("DOMContentLoaded", function () {
    const allYearCheckbox = document.getElementById("id_all_year");
    const startMonth = document.getElementById("id_seasonal_start_month");
    const endMonth = document.getElementById("id_seasonal_end_month");

    // If these fields aren't on the page, exit early
    if (!allYearCheckbox || !startMonth || !endMonth) {
        return;
    }

    function uncheckAllYear() {
        if (allYearCheckbox.checked) {
            allYearCheckbox.checked = false;
        }
    }

    startMonth.addEventListener("change", uncheckAllYear);
    endMonth.addEventListener("change", uncheckAllYear);
});



// ------------------------------------------------------------
// 2. AJAX Modal: Create Garden Bed without reloading the page
//
//    This block handles the Option A workflow:
//    - Intercepts the modal form submission
//    - Sends it via fetch() with the AJAX header
//    - Receives JSON instead of a redirect
//    - Updates the bed dropdown (if present)
//    - Closes the modal
//
//    IMPORTANT:
//    The modal exists on multiple pages (beds list, plant create,
//    plant edit), but the bed dropdown ONLY exists on plant pages.
//    So we attach the AJAX handler whenever the modal exists,
//    and only update the dropdown if it is present.
// ------------------------------------------------------------
document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("createBedModal");
    const modalForm = document.getElementById("bedCreateForm");
    const bedSelect = document.getElementById("id_bed");

    // Guard clause:
    // If the modal OR the form doesn't exist, this page doesn't
    // support inline bed creation — exit safely.
    if (!modal || !modalForm) {
        return;
    }

    // Bootstrap modal instance (used to close the modal programmatically)
    const bsModal = bootstrap.Modal.getOrCreateInstance(modal);

    // Intercept the modal form submission
    modalForm.addEventListener("submit", async function (e) {
        e.preventDefault();  // Prevent full page reload

        const formData = new FormData(modalForm);

        // Send AJAX request to Django
        const response = await fetch(modalForm.action, {
            method: "POST",
            body: formData,
            headers: {
                // This header tells Django: "This is an AJAX request"
                "X-Requested-With": "XMLHttpRequest"
            }
        });

        const data = await response.json();

        // If Django returned success, update the UI
        if (data.success) {

            // Only update the dropdown if it exists (plant pages)
            if (bedSelect) {
                const option = new Option(data.name, data.id, true, true);
                bedSelect.add(option);
            }

            // Close the modal
            bsModal.hide();

            // Reset the modal form for next time
            modalForm.reset();
        }
    });
});


// -------------------------------------------------------------
// Image Delete Button Behaviour
// -------------------------------------------------------------
// This script replaces Django's "Clear" checkbox with a proper
// "Delete image" button that matches your app's styling.
//
// When the user clicks "Delete image":
//   - The hidden Clear checkbox is ticked
//   - The thumbnail preview disappears
//   - A red "Image will be removed" message appears
//
// If the user clicks the button again (toggle behaviour):
//   - The checkbox is unticked
//   - The preview returns
//   - The message disappears
//
// This keeps Django's deletion logic intact while providing
// modern, intuitive UX.
// -------------------------------------------------------------

document.addEventListener("DOMContentLoaded", function () {
    const clearCheckbox = document.querySelector("#id_image-clear");
    const deleteBtn = document.querySelector("#delete-image-btn");
    const previewBlock = document.getElementById("current-image-block");
    const removedMsg = document.getElementById("image-removed-msg");

    if (clearCheckbox && deleteBtn) {
        deleteBtn.addEventListener("click", function () {
            const isDeleting = !clearCheckbox.checked;

            // Toggle checkbox
            clearCheckbox.checked = isDeleting;

            // Toggle preview visibility
            if (previewBlock) {
                previewBlock.style.display = isDeleting ? "none" : "block";
            }

            // Toggle "image will be removed" message
            if (removedMsg) {
                removedMsg.style.display = isDeleting ? "block" : "none";
            }

            // Update button text for clarity
            deleteBtn.textContent = isDeleting ? "Undo delete" : "Delete image";
        });
    }
});
