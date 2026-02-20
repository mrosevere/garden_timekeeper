// core/dom.js

export function qs(selector, parent = document) {
    return parent.querySelector(selector);
}

export function qsa(selector, parent = document) {
    return Array.from(parent.querySelectorAll(selector));
}

export function clear(el) {
    while (el.firstChild) {
        el.removeChild(el.firstChild);
    }
}
