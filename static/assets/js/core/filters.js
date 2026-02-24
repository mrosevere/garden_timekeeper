// core/filters.js
/* jshint esversion: 11 */

import { normalise } from "./utils.js";

export function applyFilters(tasks, { search, status, season }) {
    return tasks.filter(task => {
        const nameMatch = !search || normalise(task.name).includes(normalise(search));
        const statusMatch = !status || task.status === status;
        const seasonMatch = !season || task.season === season;

        return nameMatch && statusMatch && seasonMatch;
    });
}
