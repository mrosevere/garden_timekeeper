# Manual Testing Documentation

This document outlines the full manual testing process for the **Garden Timekeeper** application.  
All tests were performed manually on both the deployed Heroku site and the local development environment.

Testing covers:

- User stories  
- CRUD functionality  
- Forms and validation  
- Sorting and filtering  
- Responsive behaviour  
- Accessibility  
- Browser compatibility  
- Deployment behaviour  
- Known issues  

---

# 1. User Story Testing

| User Story | Test Steps | Expected Result | Actual Result | Status |
|-----------|------------|----------------|----------------|--------|
| As a user, I can register an account | Visit signup page, enter valid details | Account created, redirected to login | Works as expected | Pass |
| As a user, I can log in | Enter valid credentials | Logged in and redirected | Works as expected | Pass |
| As a user, I can log out | Click Logout | Session ends, redirected | Works as expected | Pass |
| As a user, I can view my garden beds | Navigate to Beds page | Beds displayed | Works as expected | Pass |
| As a user, I can add a bed | Click Add Bed, submit form | Bed created | Works as expected | Pass |
| As a user, I can edit a bed | Edit bed, submit | Bed updated | Works as expected | Pass |
| As a user, I can delete a bed | Confirm delete modal | Bed removed | Works as expected | Pass |
| As a user, I can sort beds | Click table headers | Table sorts | Works as expected | Pass |
| As a user, I can filter beds | Use search + location filters | Results update | Works as expected | Pass |
| As a user, I can view plants | Navigate to Plants page | Plants displayed | Works as expected | Pass |
| As a user, I can add/edit/delete plants | Use CRUD forms | Plant created/updated/deleted | Works as expected | Pass |
| As a user, I can add notes to a plant | Enter formatted text in Summernote | Notes saved and displayed | Works as expected | Pass |
| As a user, I can manage tasks | Add/edit/delete tasks | Tasks updated | Works as expected | Pass |
| As a user, I can track watering | Add/edit/delete watering entries | Entries updated | Works as expected | Pass |

---

# 2. CRUD Testing

## Beds

| Action | Steps | Expected | Actual | Status |
|--------|--------|----------|---------|--------|
| Create | Fill form | New bed appears | Works | Pass |
| Read | View bed list/detail | Correct data shown | Works | Pass |
| Update | Edit bed | Changes saved | Works | Pass |
| Delete | Confirm modal | Bed removed | Works | Pass |

## Plants

| Action | Steps | Expected | Actual | Status |
|--------|--------|----------|---------|--------|
| Create | Fill form | New plant appears | Works | Pass |
| Read | View plant list/detail | Correct data shown | Works | Pass |
| Update | Edit plant | Changes saved | Works | Pass |
| Delete | Confirm modal | Plant removed | Works | Pass |

## Tasks

| Action | Steps | Expected | Actual | Status |
|--------|--------|----------|---------|--------|
| Create | Add task | Task appears | Works | Pass |
| Read | View task list | Correct data shown | Works | Pass |
| Update | Edit task | Changes saved | Works | Pass |
| Delete | Confirm modal | Task removed | Works | Pass |

## Watering

| Action | Steps | Expected | Actual | Status |
|--------|--------|----------|---------|--------|
| Create | Add watering entry | Entry appears | Works | Pass |
| Read | View watering list | Correct data shown | Works | Pass |
| Update | Edit entry | Changes saved | Works | Pass |
| Delete | Confirm modal | Entry removed | Works | Pass |

---

# 3. Form Validation Testing

| Form | Invalid Input | Expected | Actual | Status |
|------|---------------|----------|---------|--------|
| Bed form | Empty name | Error message | Displayed | Pass |
| Plant form | Missing required fields | Error message | Displayed | Pass |
| Task form | Invalid dates | Validation error | Displayed | Pass |
| Watering form | Missing date | Error message | Displayed | Pass |

---

# 4. Sorting & Filtering Testing

| Feature | Test | Expected | Actual | Status |
|---------|-------|----------|---------|--------|
| Bed sorting | Click column headers | Asc/desc toggle | Works | Pass |
| Plant sorting | Click column headers | Asc/desc toggle | Works | Pass |
| Search | Enter text | Matching results only | Works | Pass |
| Filters | Select dropdowns | Results update | Works | Pass |

---

# 5. Responsive Testing

Tested using Chrome DevTools and physical devices.

| Device Size | Expected Behaviour | Actual | Status |
|-------------|--------------------|--------|--------|
| Mobile | Cards instead of tables, collapsible filters | Works | Pass |
| Tablet | Hybrid layout | Works | Pass |
| Desktop | Full table layout | Works | Pass |

---

# 6. Accessibility Testing

| Test | Expected | Actual | Status |
|------|----------|---------|--------|
| Keyboard navigation | All interactive elements reachable | Works | Pass |
| ARIA labels | Buttons/links labelled | Works | Pass |
| Colour contrast | Meets WCAG AA | Pass | Pass |
| Lighthouse score | 90+ | Achieved | Pass |
| Alt text | All images have alt | Works | Pass |

---

# 7. Browser Compatibility

| Browser | Result |
|---------|--------|
| Chrome | Pass |
| Firefox | Pass |
| Edge | Pass |
| Safari (iOS) | Pass |
| Chrome Android | Pass |

---

# 8. HTML & CSS Validation

| Page | Validator | Result |
|------|-----------|--------|
| All templates | W3C HTML | Pass (except Summernote content) |
| CSS | W3C CSS | Pass |

### Known HTML Issue  
Summernote allows users to enter rich HTML (headings, inline styles, deprecated tags).  
This may trigger validation warnings.  
These originate from user-generated content, not template structure.

---

# 9. Deployment Testing (Heroku)

| Test | Expected | Actual | Status |
|------|----------|---------|--------|
| App loads | Loads normally | Works | Pass |
| Dyno sleep | First load slow | Works | Pass |
| Database reconnect | Occasional 500 due to free Postgres SSL reconnect | Documented | Pass (with note) |

---

# 10. Known Issues

### Heroku Free Tier Database Reconnect  
Occasional 500 errors immediately after dyno wake due to:

```
django.db.utils.OperationalError: SSL connection has been closed unexpectedly
```

Documented in README.  
Not caused by application code.

### Summernote HTML Validation  
User-entered HTML may trigger W3C warnings.  
Documented and expected.

---