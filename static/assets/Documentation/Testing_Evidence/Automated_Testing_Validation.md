# Automated Testing Documentation

This document provides full evidence of the automated testing implemented for the **Garden Timekeeper** application. Automated tests complement the manual testing documented in `manual_testing.md` by verifying core logic, model behaviour, view permissions, and form validation using Django’s built‑in test framework.

All tests were executed using Django’s test runner and measured with `coverage`:

- Test execution: `python manage.py test`
- Coverage execution: `coverage run manage.py test`

The test suite covers the **core**, **accounts**, and **tasks** functionality delivered in the project.

---

## 1. Overview of Automated Testing Strategy

Automated tests were written to validate:

- Model behaviour (string methods, defaults, relationships)
- Form validation (required fields, invalid input, edge cases)
- View permissions (login required, user‑specific access)
- URL routing (correct resolution of named routes)
- Business logic (task status updates, date calculations)
- Template rendering (correct templates used for each view)
- Custom template tags and utility functions

The goal was to ensure that critical logic remains stable even as the application evolves.

---

## 2. Running the Test Suite

All tests were executed using Django’s built‑in test runner:

- `python manage.py test`

The test suite completed successfully with:

- **142 tests run**
- **0 failures**
- **0 errors**
- **All tests passing (100% pass rate)**

A screenshot of the terminal output is included in the README.

---

## 3. Test Coverage Summary

Code coverage was measured using `coverage`:

- Run tests with coverage: `coverage run manage.py test`
- Generate summary: `coverage report -m`
- Generate HTML report: `coverage html` (output in `htmlcov/`)

### 3.1 Overall Coverage

| Metric                | Value  |
|-----------------------|--------|
| Total statements      | 1599   |
| Missing statements    | 87     |
| Overall coverage      | **95%** |

### 3.2 Coverage Highlights

- **Core application logic (models, views, forms):** 88–100% coverage
- **All test modules:** 100%
- **Template tags:** 100%
- **URL routing modules:** 91–100%
- **Settings and admin modules:** high coverage, as expected

The remaining uncovered lines are primarily:

- Defensive or fallback branches
- Rare error paths
- Settings/startup code
- Non‑critical helper logic

None of these affect the correctness of core user workflows.

---

## 4. Model Tests

### 4.1 Bed Model Tests

**Tests performed:**

- String representation returns bed name
- Beds are linked to the correct user
- Optional fields (e.g. location) behave correctly
- Beds cannot be created without a name

**Status:** All bed model tests passed.

---

### 4.2 Plant Model Tests

**Tests performed:**

- String representation returns plant name
- Plants correctly associate with beds and owners
- Notes field accepts rich text content
- Missing required fields trigger validation errors

**Status:** All plant model tests passed.

---

### 4.3 Task Model Tests

**Tests performed:**

- String representation returns task name/type
- Due date calculations (today, overdue, upcoming)
- Status updates (done, skipped)
- Tasks correctly link to plants and beds

**Status:** All task model tests passed.

---

## 5. Form Tests

### 5.1 BedForm Tests

- Missing name → validation error
- Valid data → form is valid
- Duplicate names per user → validation error

### 5.2 PlantForm Tests

- Missing name → validation error
- Missing type → validation error
- Valid data → form is valid

### 5.3 TaskForm Tests

- Missing due date → validation error
- Invalid date formats → validation error
- Valid data → form is valid

**Status:** All form tests passed.

---

## 6. View Tests

### 6.1 Authentication and Permissions

For all protected views:

- Anonymous users are redirected to login (302)
- Authenticated users can access their own beds, plants, and tasks
- Users cannot access or modify other users’ beds, plants, or tasks (404 where appropriate)

### 6.2 CRUD View Tests

For each model (Bed, Plant, Task):

- List views load the correct template and context
- Detail views load the correct object and return 200
- Create views save valid data and redirect appropriately
- Edit views update existing objects and redirect appropriately
- Delete views remove objects and redirect to the expected page

### 6.3 Template Rendering

Each view was tested to ensure:

- The correct template is used
- The correct context variables are passed
- The correct HTTP status codes are returned

**Status:** All view tests passed.

---

## 7. URL Resolution Tests

Named URLs were tested using Django’s URL utilities to ensure:

- URL names resolve to the correct views
- URL patterns accept expected parameters
- No broken or unused routes remain

**Status:** All URL tests passed.

---

## 8. Business Logic Tests

### 8.1 Task Status Logic

- Marking a task as **done** updates the status correctly
- Marking a task as **skipped** updates the status correctly
- Completed or skipped tasks no longer appear in dashboard queries

### 8.2 Due/Overdue Logic

- Tasks due today appear in the “Due Today” section
- Tasks due in the next 7 days appear in the “Upcoming” section
- Past‑due tasks appear in the “Overdue” section
- Completed/skipped tasks are excluded from active task lists

**Status:** All business logic tests passed.

---

## 9. Template Tag and Utility Tests

Custom template tags and utilities were tested to ensure:

- Month filters return correct month names and labels
- Navigation tags correctly highlight the active section
- Helper functions behave consistently across views

**Status:** All template tag and utility tests passed.

---

## 10. Quality and Reliability Assessment

The combination of:

- A large, well‑structured test suite
- Full CRUD and permission coverage
- High branch coverage across views and forms
- Thorough model and template tag testing
- A **95% overall coverage score**

provides strong evidence that the system is robust, secure, and behaves correctly under all expected usage scenarios.

Automated tests also helped validate recent security and configuration changes (such as SSL‑related settings), ensuring that production‑grade configuration did not regress application behaviour.

---

## 11. Conclusion

The **Garden Timekeeper** application demonstrates a high level of automated test maturity. With **142 passing tests** and **95% code coverage**, the system is thoroughly validated, and the test suite provides strong confidence in the correctness, stability, and maintainability of the application.
