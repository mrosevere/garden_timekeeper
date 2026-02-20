// core/pagination.js

export class Paginator {
    constructor(items, perPage = 3) {
        this.items = items;
        this.perPage = perPage;
        this.currentPage = 1;
    }

    setItems(items) {
        this.items = items;
        this.currentPage = 1;
    }

    totalPages() {
        return Math.max(1, Math.ceil(this.items.length / this.perPage));
    }

    getPageItems() {
        const start = (this.currentPage - 1) * this.perPage;
        return this.items.slice(start, start + this.perPage);
    }

    goToPage(page) {
        this.currentPage = Math.min(Math.max(1, page), this.totalPages());
    }

    next() {
        this.goToPage(this.currentPage + 1);
    }

    prev() {
        this.goToPage(this.currentPage - 1);
    }
}
