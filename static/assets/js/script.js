// Reserved for global behaviours (navbar, modals, etc.)
// Plant Detail Page logic lives in plant_detail.js


// Confirm the JS bundle is loaded
// console.log("Garden Timekeeper JS loaded");

/* global bootstrap, $ */
/* exported initSummernoteWithBootstrap5 */
/* jshint esversion: 11 */
/* jshint -W064 */


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
// 3. Image Delete Button Behaviour
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


// -------------------------------------------------------------
// 4. Summernote Initialiser (Bootstrap 5 Compatible)
//
// This helper function applies a fully‑patched Summernote editor
// to any field selector. Summernote was originally built for
// Bootstrap 3/4, so Bootstrap 5 breaks several behaviours:
//   - Dropdowns no longer open/close correctly
//   - Tooltips fail to initialise
//   - The Style dropdown stays open after selection
//   - Heading 2 does not apply due to a Summernote quirk
//
// This function:
//   • Initialises Summernote with a consistent toolbar
//   • Rewrites legacy data‑toggle attributes to Bootstrap 5
//   • Re‑initialises tooltips and dropdowns using Bootstrap 5 APIs
//   • Forces the Style dropdown to close after selecting an option
//   • Overrides the broken H2 behaviour with a reliable formatBlock call
//
// Usage:
//   initSummernoteWithBootstrap5('#id_notes');
//   initSummernoteWithBootstrap5('#id_task_notes', 300);
//
// This keeps all Summernote fixes in one place and ensures that
// any page using a notes field behaves consistently.
// -------------------------------------------------------------

function initSummernoteWithBootstrap5(selector, height = 200) {
    $(selector).summernote({
        height: height,
        toolbar: [
            ['style', ['style']],
            ['font', ['bold', 'italic', 'underline', 'clear']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['insert', ['link', 'picture']],
            ['view', ['fullscreen']]
        ],
        callbacks: {
            onInit: function() {
                const $editor = $(selector).next('.note-editor');

                // Fix dropdowns
                $editor.find('[data-toggle="dropdown"]')
                    .attr('data-bs-toggle', 'dropdown')
                    .removeAttr('data-toggle');

                // Fix tooltips
                $editor.find('[data-toggle="tooltip"]')
                    .attr('data-bs-toggle', 'tooltip')
                    .removeAttr('data-toggle');

                // Reinitialise Bootstrap tooltips
                $editor.find('[data-bs-toggle="tooltip"]').each(function() {
                    /* jshint -W064 */
                    new bootstrap.Tooltip(this);
                    /* jshint +W064 */
                });

                // Reinitialise Bootstrap dropdowns
                $editor.find('[data-bs-toggle="dropdown"]').each(function() {
                    /* jshint -W064 */
                    new bootstrap.Dropdown(this);
                    /* jshint +W064 */
                });

                // Close Style dropdown after selection
                $editor.find('.note-dropdown-menu a').on('click', function () {
                    const dropdownButton = $(this)
                        .closest('.note-btn-group')
                        .find('[data-bs-toggle="dropdown"]')[0];

                    const dropdown = bootstrap.Dropdown.getInstance(dropdownButton);
                    if (dropdown) dropdown.hide();
                });

                // Fix Heading 2 not applying
                $editor.find('.note-dropdown-menu a[data-value="h2"]').on('click', function (e) {
                    e.preventDefault();
                    $(selector).summernote('formatBlock', 'H2');
                });
            }
        }
    });
}
