// core/utils.js

// Normalise text for case-insensitive search
export function normalise(text) {
    return text ? text.toString().trim().toLowerCase() : "";
}

// Debounce helper (prevents firing search on every keystroke)
export function debounce(fn, delay = 200) {
    let timer = null;
    return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => fn(...args), delay);
    };
}
