### Custom JavaScript Architecture

The project includes a small set of modular JavaScript files located in `static/js/core/`.  
These scripts enhance the user experience by providing client‑side interactivity, instant feedback, and lightweight UI behaviour that complements Django’s server‑side logic.

The JS is intentionally split into focused modules to keep the codebase maintainable, testable, and easy to extend.

```
static/js/core/
│── dom.js
│── filters.js
│── pagination.js
│── utils.js
│── plant_detail.js
└── script.js
```


---

### Why custom JavaScript was needed

Django handles server‑side rendering and routing, but several parts of the UI benefit from client‑side enhancements:

- **Instant filtering** of tables and lists without a page reload  
- **Client‑side pagination controls** for long lists  
- **DOM helpers** for toggling UI elements  
- **Plant detail interactions**, such as expanding notes or toggling sections  
- **Reusable utilities** shared across multiple pages  

These behaviours are intentionally lightweight — no frameworks, no build tools — just clean, modular JavaScript that integrates seamlessly with Django templates.

---

## Module Overview

### `utils.js`
A collection of small helper functions used across multiple modules.

Typical responsibilities:
- string normalisation  
- safe element selection  
- debouncing user input  
- shared formatting helpers  

This keeps logic DRY and avoids repeating common patterns.

---

### `dom.js`
Provides safe, reusable DOM manipulation helpers.

Examples include:
- toggling classes  
- showing/hiding elements  
- attaching event listeners with fallback checks  
- reading data attributes  

This module abstracts away repetitive DOM boilerplate and keeps other modules focused on behaviour rather than low‑level manipulation.

---

### `filters.js`
Adds **client‑side filtering** to tables and lists.

Used for:
- filtering plants  
- filtering beds  
- filtering tasks  
- instant search without reloading the page  

Key features:
- debounced input handling  
- case‑insensitive matching  
- works with paginated tables  
- updates results instantly as the user types  

This creates a fast, dashboard‑like experience.

---

### `pagination.js`
Handles client‑side pagination controls.

Responsibilities:
- enabling/disabling next/previous buttons  
- scrolling to the top of the list when changing pages  
- syncing pagination state with filters  
- ensuring consistent behaviour across all list views  

This keeps long lists manageable without requiring server‑side pagination reloads.

---

### `plant_detail.js`
Contains behaviour specific to the plant detail page.

Examples:
- expanding/collapsing long notes  
- toggling task sections  
- enhancing the UX of the plant detail layout  

This keeps page‑specific logic isolated from global scripts.

---

### `script.js`
The main entry point that initialises all other modules.

Responsibilities:
- running setup functions on page load  
- attaching global event listeners  
- coordinating interactions between modules  
- ensuring modules only run on pages where they are needed  

This file acts as the “glue” that ties the JS architecture together.

---

## How the JS integrates with Django

Each Django template includes only the scripts it needs, keeping pages lightweight:

```django
{% load static %}
<script src="{% static 'js/core/utils.js' %}"></script>
<script src="{% static 'js/core/dom.js' %}"></script>
<script src="{% static 'js/core/filters.js' %}"></script>
<script src="{% static 'js/core/pagination.js' %}"></script>
<script src="{% static 'js/core/plant_detail.js' %}"></script>
<script src="{% static 'js/core/script.js' %}"></script>
```
Because the modules are small and dependency‑free, they load instantly and work across all modern browsers.

### Summary

This modular JS architecture provides:
- Fast, responsive UI behaviour without heavy frameworks
- Clean separation of concerns
- Reusable utilities across multiple pages
- Minimal bundle size
- Easy future extension (e.g., adding animations, more filters, or dashboard widgets)

It strikes a balance between Django’s server‑side strengths and modern client‑side interactivity, resulting in a polished, professional user experience.