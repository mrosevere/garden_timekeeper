// plant_detail.js
/* jshint esversion: 11 */

// ---------------------------------------------------------
// Imports
// ---------------------------------------------------------
import { qs, qsa, clear } from "./core/dom.js";
import { applyFilters } from "./core/filters.js";
import { Paginator } from "./core/pagination.js";
import { debounce } from "./core/utils.js";

document.addEventListener("DOMContentLoaded", () => {

    // ---------------------------------------------------------
    // 1. Extract all tasks from DOM (table rows + mobile cards)
    // ---------------------------------------------------------
    const rows = qsa("#plant-tasks-table tbody tr");
    const cards = qsa(".d-md-none .card");

    const tasks = rows.map((row, index) => {
        const card = cards[index];

        return {
            id: index,
            name: row.getAttribute("data-task-name") || "",
            status: row.getAttribute("data-status") || "",
            season: row.getAttribute("data-season") || "",
            frequency: row.getAttribute("data-frequency") || "",
            next_due: row.getAttribute("data-next-due") || "",
            dom: { row, card }
        };
    });

    // ---------------------------------------------------------
    // 2. Sorting state
    // ---------------------------------------------------------
    let currentSort = { key: "next_due", direction: "asc" };

    const sortableHeaders = qsa("th.sortable");

    // Apply default sort styling to the correct header
    const defaultHeader = qs('th.sortable[data-sort="next_due"]');
    if (defaultHeader) {
        defaultHeader.classList.add("sort-asc");
        const icon = defaultHeader.querySelector("i");
        if (icon) icon.className = "fa-solid fa-arrow-up-long";
    }

    function resetSortIcons() {
        sortableHeaders.forEach(th => {
            const icon = th.querySelector("i");
            if (icon) icon.className = "fa-solid fa-arrow-up-long opacity-0";
            th.classList.remove("sort-asc", "sort-desc");
        });
    }

    function sortTasks(items) {
        if (!currentSort.key || !currentSort.direction) return items;

        const sorted = [...items].sort((a, b) => {
            let valA = a[currentSort.key];
            let valB = b[currentSort.key];

            // Special case: next_due (date)
            if (currentSort.key === "next_due") {
                valA = valA || "9999-12-31";
                valB = valB || "9999-12-31";
            }

            if (valA < valB) return currentSort.direction === "asc" ? -1 : 1;
            if (valA > valB) return currentSort.direction === "asc" ? 1 : -1;
            return 0;
        });

        return sorted;
    }

    sortableHeaders.forEach(th => {
        th.addEventListener("click", () => {
            const key = th.dataset.sort;

            if (currentSort.key === key) {
                currentSort.direction = currentSort.direction === "asc" ? "desc" : "asc";
            } else {
                currentSort.key = key;
                currentSort.direction = "asc";
            }

            resetSortIcons();

            th.classList.add(
                currentSort.direction === "asc" ? "sort-asc" : "sort-desc"
            );

            const icon = th.querySelector("i");
            if (icon) {
                icon.className =
                    currentSort.direction === "asc"
                        ? "fa-solid fa-arrow-up-long"
                        : "fa-solid fa-arrow-down-long";
            }

            paginator.setItems(applyAllFiltersAndSorting());
            paginator.goToPage(1);
            render();
        });
    });

    // ---------------------------------------------------------
    // 3. Initialise paginator
    // ---------------------------------------------------------
    const paginator = new Paginator(tasks, 3);

    // ---------------------------------------------------------
    // 4. Combined filtering + sorting pipeline
    // ---------------------------------------------------------
    function applyAllFiltersAndSorting() {
        const search = qs("#task-search")?.value || "";
        const status = qs("#status-filter")?.value || "";
        const season = qs("#season-filter")?.value || "";

        let filtered = applyFilters(tasks, { search, status, season });
        filtered = sortTasks(filtered);

        return filtered;
    }

    // ---------------------------------------------------------
    // 5. Rendering function (UPDATED WITH NULL-SAFE GUARD)
    // ---------------------------------------------------------
    function render() {
        const tableBody = qs("#plant-tasks-table tbody");
        const cardContainer = qs(".d-md-none");

        // ---------------------------------------------------------
        // SAFETY CHECK:
        // If the plant has NO tasks, the template does not render
        // the table or mobile card container. Without this guard,
        // calling clear(null) would throw:
        // "Cannot read properties of null (reading 'firstChild')"
        // ---------------------------------------------------------
        if (!tableBody || !cardContainer) {
            return;  // Nothing to render — exit safely
        }

        // Clear existing DOM content
        clear(tableBody);
        clear(cardContainer);

        const pageItems = paginator.getPageItems();

        // Insert rows/cards for this page
        pageItems.forEach(task => {
            tableBody.appendChild(task.dom.row);
            cardContainer.appendChild(task.dom.card);
        });

        renderPaginationControls();
    }

    // ---------------------------------------------------------
    // 6. Pagination controls
    // ---------------------------------------------------------
    function renderPaginationControls() {
        const container = qs("#task-pagination");
        if (!container) return;

        clear(container);

        const total = paginator.totalPages();

        const prevBtn = document.createElement("button");
        prevBtn.className = "btn btn-outline-secondary btn-sm me-2";
        prevBtn.textContent = "Previous";
        prevBtn.disabled = paginator.currentPage === 1;
        prevBtn.onclick = () => {
            paginator.prev();
            render();
        };

        const nextBtn = document.createElement("button");
        nextBtn.className = "btn btn-outline-secondary btn-sm";
        nextBtn.textContent = "Next";
        nextBtn.disabled = paginator.currentPage === total;
        nextBtn.onclick = () => {
            paginator.next();
            render();
        };

        const info = document.createElement("span");
        info.className = "mx-3 text-muted small";
        info.textContent = `Page ${paginator.currentPage} of ${total}`;

        container.appendChild(prevBtn);
        container.appendChild(info);
        container.appendChild(nextBtn);
    }

    // ---------------------------------------------------------
    // 7. Filtering logic
    // ---------------------------------------------------------
    function updateFilters() {
        paginator.setItems(applyAllFiltersAndSorting());
        paginator.goToPage(1);
        render();
    }

    qs("#task-search")?.addEventListener("input", debounce(updateFilters, 150));
    qs("#status-filter")?.addEventListener("change", updateFilters);
    qs("#season-filter")?.addEventListener("change", updateFilters);

    // ---------------------------------------------------------
    // Initial render
    // ---------------------------------------------------------
    paginator.setItems(applyAllFiltersAndSorting());
    render();
});
