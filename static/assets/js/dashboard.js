// dashboard.js
/* jshint esversion: 11 */

import { qs, qsa, clear } from "./core/dom.js";
import { Paginator } from "./core/pagination.js";
import { debounce } from "./core/utils.js";

document.addEventListener("DOMContentLoaded", () => {
    // ---------------------------------------------------------
    // 1. Extract tasks from DOM (desktop rows + mobile cards)
    // ---------------------------------------------------------
    const rows = qsa("#dashboard-table-body tr");
    const cards = qsa("#dashboard-cards .dashboard-card");

    const tasks = rows.map((row, index) => {
        const card = cards[index] || null;

        return {
            id: index,
            name: row.getAttribute("data-task-name") || "",
            plant: row.getAttribute("data-plant") || "",
            bed: row.getAttribute("data-bed") || "",
            status: row.getAttribute("data-status") || "",
            frequency: row.getAttribute("data-frequency") || "",
            next_due: row.getAttribute("data-next-due") || "",
            dom: { row, card }
        };
    });

    // If there are no tasks, nothing else to do
    if (!tasks.length) return;

    // ---------------------------------------------------------
    // 2. Sorting state
    // ---------------------------------------------------------
    let currentSort = { key: "next_due", direction: "asc" };

    const sortableHeaders = qsa("th.sortable");

    // ---------------------------------------------------------
    // Default sort indicator (same behaviour as Plant Detail)
    // ---------------------------------------------------------
    const defaultHeader = qs('th.sortable[data-sort="next_due"]');
    if (defaultHeader) {
        defaultHeader.classList.add("sort-asc");
        const icon = defaultHeader.querySelector("i");
        if (icon) icon.className = "fa-solid fa-arrow-up-long ms-1";
    }


    function resetSortIcons() {
        sortableHeaders.forEach(th => {
            const icon = th.querySelector("i");
            if (icon) icon.className = "fa-solid fa-arrow-up-long opacity-0 ms-1";
            th.classList.remove("sort-asc", "sort-desc");
        });
    }

    function sortTasks(items) {
        if (!currentSort.key || !currentSort.direction) return items;

        const sorted = [...items].sort((a, b) => {
            let valA = a[currentSort.key] || "";
            let valB = b[currentSort.key] || "";

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
                        ? "fa-solid fa-arrow-up-long ms-1"
                        : "fa-solid fa-arrow-down-long ms-1";
            }

            paginator.setItems(applyAllFiltersAndSorting());
            paginator.goToPage(1);
            render();
        });
    });

    // ---------------------------------------------------------
    // 3. Initialise paginator
    // ---------------------------------------------------------
    const paginator = new Paginator(tasks, 3); // x per page; 

    // ---------------------------------------------------------
    // 4. Filtering + search pipeline
    // ---------------------------------------------------------
    function applyAllFiltersAndSorting() {
        const search = qs("#dashboard-search")?.value.toLowerCase().trim() || "";
        const statusFilter = qs("#dashboard-status-filter")?.value || "";

        let filtered = tasks.filter(task => {
            // Status filter
            if (statusFilter && task.status !== statusFilter) {
                return false;
            }

            // Search across task, plant, bed
            if (search) {
                const haystack = `${task.name} ${task.plant} ${task.bed}`;
                if (!haystack.includes(search)) {
                    return false;
                }
            }

            return true;
        });

        filtered = sortTasks(filtered);
        return filtered;
    }

    // ---------------------------------------------------------
    // 5. Rendering function
    // ---------------------------------------------------------
    function render() {
        const tableBody = qs("#dashboard-table-body");
        const cardContainer = qs("#dashboard-cards");

        // If either container is missing, bail safely
        if (!tableBody || !cardContainer) return;

        clear(tableBody);
        clear(cardContainer);
        const row = document.createElement("div");
        row.className = "row";
        cardContainer.appendChild(row);

        const pageItems = paginator.getPageItems();

        pageItems.forEach(task => {
            // Desktop row
            tableBody.appendChild(task.dom.row);

            // Mobile card (if present)
            if (task.dom.card) {
                // Wrap in a col-12 like the template originally did
                const col = document.createElement("div");
                col.className = "col-12";
                col.appendChild(task.dom.card);
                row.appendChild(col);
            }
        });

        renderPaginationControls();
    }

    // ---------------------------------------------------------
    // 6. Pagination controls
    // ---------------------------------------------------------
    function renderPaginationControls() {
        const container = qs("#dashboard-pagination");
        if (!container) return;

        clear(container);

        const total = paginator.totalPages();
        if (total <= 1) return;

        const current = paginator.currentPage;

        // Helper to create Bootstrap pagination items
        function makePageItem({ label, disabled = false, active = false, onClick = null }) {
            const li = document.createElement("li");
            li.className = "page-item";

            // Disabled or active items use <span>
            if (disabled || active) {
                if (disabled) li.classList.add("disabled");
                if (active) li.classList.add("active");

                const span = document.createElement("span");
                span.className = "page-link";

                // Use innerHTML only for HTML entities
                if (typeof label === "number") {
                    span.textContent = label;
                } else {
                    span.innerHTML = label;
                }

                li.appendChild(span);
                return li;
            }

            // Clickable items use <a>
            const a = document.createElement("a");
            a.className = "page-link";
            a.href = "#";

            if (typeof label === "number") {
                a.textContent = label;
            } else {
                a.innerHTML = label;
            }

            a.onclick = (e) => {
                e.preventDefault();
                if (onClick) onClick();
            };

            li.appendChild(a);
            return li;
        }

        // Create <nav> wrapper
        const nav = document.createElement("nav");
        nav.setAttribute("aria-label", "Dashboard pagination");

        // Create <ul> for Bootstrap pagination
        const ul = document.createElement("ul");
        ul.className = "pagination justify-content-center flex-wrap gap-1 pagination-sm";

        // First (««)
        ul.appendChild(
            makePageItem({
                label: "&laquo;&laquo;",
                disabled: current === 1,
                onClick: () => {
                    paginator.goToPage(1);
                    render();
                }
            })
        );

        // Previous («)
        ul.appendChild(
            makePageItem({
                label: "&laquo;",
                disabled: current === 1,
                onClick: () => {
                    paginator.goToPage(current - 1);
                    render();
                }
            })
        );

        // Page numbers
        for (let i = 1; i <= total; i++) {
            ul.appendChild(
                makePageItem({
                    label: i,
                    active: i === current,
                    onClick: () => {
                        paginator.goToPage(i);
                        render();
                    }
                })
            );
        }

        // Next (»)
        ul.appendChild(
            makePageItem({
                label: "&raquo;",
                disabled: current === total,
                onClick: () => {
                    paginator.goToPage(current + 1);
                    render();
                }
            })
        );

        // Last (»»)
        ul.appendChild(
            makePageItem({
                label: "&raquo;&raquo;",
                disabled: current === total,
                onClick: () => {
                    paginator.goToPage(total);
                    render();
                }
            })
        );

        // Attach <ul> to <nav>, then into container
        nav.appendChild(ul);
        container.appendChild(nav);
    }

    // ---------------------------------------------------------
    // 7. Filtering events
    // ---------------------------------------------------------
    function updateFilters() {
        paginator.setItems(applyAllFiltersAndSorting());
        paginator.goToPage(1);
        render();
    }

    qs("#dashboard-search")?.addEventListener("input", debounce(updateFilters, 150));
    qs("#dashboard-status-filter")?.addEventListener("change", updateFilters);

    // ---------------------------------------------------------
    // Initial render
    // ---------------------------------------------------------
    paginator.setItems(applyAllFiltersAndSorting());
    render();
});
