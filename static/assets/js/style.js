// Debug message to confirm the JS is hooked up correctly.
console.log("Garden Timekeeper JS loaded");

// Auto‑untick "All year" when seasonal months change (issue-109)
document.addEventListener("DOMContentLoaded", function () {
    const allYearCheckbox = document.getElementById("id_all_year");
    const startMonth = document.getElementById("id_seasonal_start_month");
    const endMonth = document.getElementById("id_seasonal_end_month");

    if (!allYearCheckbox || !startMonth || !endMonth) {
        return; // Not on the task form page
    }

    function uncheckAllYear() {
        if (allYearCheckbox.checked) {
            allYearCheckbox.checked = false;
        }
    }

    startMonth.addEventListener("change", uncheckAllYear);
    endMonth.addEventListener("change", uncheckAllYear);
});
