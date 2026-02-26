# Manual Testing Documentation

This document outlines the complete manual testing performed for the **Garden Timekeeper** application. All tests were carried out on both the deployed Heroku version and the local development environment. Testing covers all major features, negative scenarios, validation behaviour, responsiveness, accessibility, and deployment reliability.


## 1. Authentication

This section covers all functionality related to user identity, access, and session management in the Garden Timekeeper application. Tests reflect the delivered implementation, including Django’s built‑in authentication flows and the custom Account page.

---

### 1.1 Registration

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Register with valid details | Fill form with unique username, email, and password | Account created, success message shown, redirected to login | Passed |
| Duplicate username (case-insensitive) | Enter an existing username | Error message: “Username already exists” | Passed |
| Duplicate email | Enter an existing email | Error message: “Email already registered” | Passed |
| Missing fields | Leave required fields blank | Field-level validation errors | Passed |
| Weak password | Enter password failing Django validators | Error message listing password requirements | Passed |
| Mismatched passwords | Enter different password and confirmation | Error message: “Passwords do not match” | Passed |
| Registration while logged in | Visit /register while authenticated | Redirect to dashboard | Passed |

---

### 1.2 Login

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Login with valid credentials | Enter correct username and password | Redirect to dashboard | Passed |
| Login with invalid password | Enter wrong password | Error message: “Invalid credentials” | Passed |
| Login with unknown username | Enter non-existent username | Error message | Passed |
| Login with blank fields | Submit empty form | Field-level validation errors | Passed |
| Login while already authenticated | Visit /login while logged in | Redirect to dashboard | Passed |
| Session ends on browser close | Login without “remember me” | Session cookie expires on close | Passed |
| Persistent session | Login with “remember me” | Session persists after browser restart | Passed |

---

### 1.3 Logout

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Logout via navbar | Click “Logout” | Session cleared, redirected to login | Passed |
| Logout via direct URL | Visit /logout | Session cleared | Passed |
| Access restricted pages after logout | Attempt /beds, /plants, /tasks | Redirect to login | Passed |

---

### 1.4 Password Reset (Forgot Password)

#### Request Reset Email

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Request reset with valid email | Enter registered email | Success message: “Email sent” | Passed |
| Request reset with unknown email | Enter unregistered email | Same success message (security best practice) | Passed |
| Request reset with blank field | Submit empty form | Validation error | Passed |

*** *NOTE:* *** The SendGrid emails normally end up in the <b>SPAM</b> folder.
#### Reset Link Behaviour

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Open valid reset link | Click link from email | Password reset form loads | Passed |
| Submit strong new password | Enter valid password | Password updated, redirected to login | Passed |
| Submit weak password | Enter invalid password | Validation errors | Passed |
| Submit mismatched passwords | Enter different new/confirm | Error shown | Passed |
| Use expired or already-used link | Open old link | Error: “Reset link invalid” | Passed |

---

### 1.5 Password Change (Logged-In Users)

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Change password with correct old password | Enter old + new password | Password updated, success message | Passed |
| Incorrect old password | Enter wrong old password | Error: “Old password incorrect” | Passed |
| Weak new password | Enter invalid password | Validation errors | Passed |
| Mismatched new passwords | Enter different new/confirm | Error shown | Passed |

---

### 1.6 Account Page (Profile)

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| View account page | Navigate to /account | Username, email, and profile info displayed | Passed |
| Update profile | Change username or email | Changes saved, success message | Passed |
| Invalid email | Enter malformed email | Validation error | Passed |
| Duplicate email | Enter another user’s email | Error: “Email already in use” | Passed |
| Access account page while logged out | Visit /account | Redirect to login | Passed |
| Attempt to update another user’s account | Manipulate form or URL | Blocked by server-side validation | Passed |

---

### 1.7 Access Control & Permissions

#### Restricted Page Access

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Access /beds while logged out | Direct URL | Redirect to login | Passed |
| Access /plants while logged out | Direct URL | Redirect to login | Passed |
| Access /tasks while logged out | Direct URL | Redirect to login | Passed |

#### Cross-User Access Protection

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Access another user’s bed | Change bed ID in URL | 404 or redirect | Passed |
| Access another user’s plant | Change plant ID in URL | 404 or redirect | Passed |
| Access another user’s task | Change task ID in URL | 404 or redirect | Passed |

---

#### CSRF Protection

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Submit form without CSRF token | 1. Open any POST form (e.g., Add Bed).<br>2. Open DevTools → Elements panel.<br>3. Locate the hidden `<input name="csrfmiddlewaretoken">`.<br>4. Delete the entire input element.<br>5. Submit the form. | Django rejects the request with **403 Forbidden** and a CSRF failure message. | Passed |
| Modify CSRF token | 1. Open any POST form.<br>2. Inspect the CSRF token input.<br>3. Replace the value with an invalid string (e.g., `FAKE123`).<br>4. Submit the form. | Django rejects the request with **403 Forbidden** due to token mismatch. | Passed |

---

### 1.8 Session & Cookie Behaviour

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Session cookie created on login | Login normally | Session cookie present | Passed |
| Cookie cleared on logout | Logout | Session cookie removed | Passed |
| Secure/HttpOnly flags (production) | Inspect cookies on Heroku | Flags correctly applied | Passed |
| Session expiry | Allow session to expire | User logged out automatically | Passed |

---

### 1.9 Usability & UX

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Clear error messages | Trigger validation errors | Errors displayed near fields | Passed |
| Focus behaviour | Submit invalid form | Focus moves to first invalid field | Passed |
| Password masking | Type password | Characters hidden | Passed |
| Show/hide password toggle | Use toggle (if implemented) | Password visibility changes | Passed |
| Keyboard navigation | Tab through form | All fields reachable in logical order | Passed |

---

## 2. Navigation & Layout

This section validates the global navigation structure, layout consistency, and user interface behaviour across all pages of the Garden Timekeeper application. Tests ensure that navigation elements update correctly based on authentication state, links route to the correct locations, and layout components behave consistently across the application.

---

### 2.1 Navbar Behaviour

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Navbar when logged out | 1. Log out.<br>2. View any page. | Navbar shows **Login**, **Register**, **Home**, **Dashboard**, **Bed List**, **Plant List** & **My Account**. | Passed |
| Navbar when logged in | 1. Log in.<br>2. View any page. | Navbar shows **Logout**, **Home**, **Dashboard**, **Bed List**, **Plant List** & **My Account**. | Passed |
| Navbar updates immediately after login | 1. Log in.<br>2. Observe navbar. | **Login**, **Register** replaced with **Logout** link. | Passed |
| Navbar updates immediately after logout | 1. Log out.<br>2. Observe navbar. | **Logout** link removed; ***Login*** & ***Register*** shown. | Passed |
| Navbar links route correctly | Click each navbar item | User is taken to the correct page. | Passed |
| Active link highlighting | Navigate through pages | Current page link is visually highlighted (active state). | Passed |
| Navbar collapses on mobile | View on small screen | Navbar collapses into hamburger menu. | Passed |
| Mobile menu expands/collapses | Tap hamburger icon | Menu opens and closes correctly. | Passed |

---

### 2.2 Footer

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Footer visible on all pages | Navigate through app | Footer consistently displayed. | Passed |
| Footer remains at bottom of viewport | View short-content pages | Footer sticks to bottom without overlapping content. | Passed |

---

### 2.3 Layout Consistency

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Page titles consistent | Visit Beds, Plants, Tasks, Dashboard | Each page displays correct title/header. | Passed |
| Consistent spacing and alignment | Compare list pages | Tables, cards, and forms follow consistent spacing and alignment. | Passed |
| Flash messages appear correctly | Trigger success/error actions | Messages appear at top, styled correctly, dismiss automatically. | Passed |
| Form layout consistent | Open Add/Edit forms across features | Labels, inputs, and buttons follow consistent styling. | Passed |
| Modal layout consistent | Trigger delete confirmation modals | Modals use consistent styling and behaviour. | Passed |

---

### 2.4 Navigation Error Handling

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Navigate to invalid URL | Enter a non-existent route | Custom 404 page displayed. | Passed |
| Attempt to access restricted page while logged out | Visit /beds, /plants, /tasks | Redirect to login page. | Passed |
| Attempt to access another user’s content | Change ID in URL | 404 or redirect (permission denied). | Passed |

---

### 2.5 Internal Link Integrity

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Links inside tables | Click plant/bed/task names | Navigate to correct detail pages. | Passed |
| “Add” buttons | Click Add Bed/Plant/Task | Navigate to correct form pages. | Passed |
| “Edit” buttons | Click Edit on any item | Navigate to correct edit form. | Passed |
| “Delete” buttons | Click Delete | Opens correct confirmation modal. | Passed |
| Dashboard task links | Click task row | Opens correct task detail page. | Passed |

---

### 2.6 Responsive Navigation Layout

*(Full responsive behaviour is covered in the Responsive Testing section, but navigation-specific behaviour is validated here.)*

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Navbar collapses on mobile | Resize to <768px | Hamburger menu appears. | Passed |
| Footer remains accessible | Resize window | Footer stays visible and does not overlap content. | Passed |
| Navigation links remain tappable | Test on mobile device | Links/buttons sized appropriately for touch. | Passed |

---

## 3. Dashboard

The Dashboard provides a consolidated view of tasks that are **due today**, **due in the next 7 days**, and **overdue**. It also supports filtering, sorting, marking tasks as done or skipped, and navigating to related Beds, Plants, and Tasks. This section validates all delivered dashboard functionality.

---

### 3.1 Display of Due, Upcoming, and Overdue Tasks

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Display tasks due today | 1. Create a task with today’s date.<br>2. Log in and view dashboard. | Task appears as **Due**. | Passed |
| Display tasks due next month | 1. Create a task due next month.<br>2. View dashboard. | Task appears as regular table row. | Passed |
| Display overdue tasks | 1. Create a task with a past due date.<br>2. View dashboard. | Task appears as an **Overdue Tasks**. | Passed |
| Empty state (no tasks due) | 1. Ensure no tasks fall within today/next 7 days/overdue.<br>2. View dashboard. | Dashboard shows a friendly empty-state message. | Passed |
| Completed tasks not shown | 1. Mark a task as done.<br>2. Refresh dashboard. | Task no longer appears in any dashboard list. | Passed |
| Skipped tasks not shown | 1. Mark a task as skipped.<br>2. Refresh dashboard. | Task no longer appears in any dashboard list. | Passed |

---

### 3.2 Filtering

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Search by bed | 1. Enter Bed name in search.<br>2. Select a specific bed. | Only tasks belonging to that bed are shown. | Passed |
| Search by plant | 1. Enter Plant name in search.<br>2. Select a plant. | Only tasks for that plant are shown. | Passed |
| Search by task | 1. Enter Task name in search.<br>2. Select a type. | Only tasks of that type are shown. | Passed |
| Clear filters | 1. Apply filters.<br>2. Click “Clear Filters”. | All dashboard tasks reappear. | Passed |

---

### 3.3 Sorting

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Sort by due date | 1. Click Due Date column header.<br>2. Click again. | Ascending/descending toggle works. | Passed |
| Sort by bed | 1. Click Bed column header.<br>2. Toggle sort. | Tasks sort alphabetically by bed. | Passed |
| Sort by plant | 1. Click Plant column header.<br>2. Toggle sort. | Tasks sort alphabetically by plant. | Passed |
| Sort by task type | 1. Click Type column header.<br>2. Toggle sort. | Tasks sort alphabetically by type. | Passed |

---

### 3.4 Pagination and Month Navigation (if applicable)

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Pagination appears when needed | 1. Create more tasks than fit on one page.<br>2. View dashboard. | Pagination controls appear. | Passed |
| Navigate between pages | 1. Click “Next”.<br>2. Click “Previous”. | Dashboard updates to correct page. | Passed |
| Change month view (if implemented) | 1. Use month navigation controls.<br>2. Switch to next/previous month. | Dashboard updates to show tasks for selected month. | Passed |

---

### 3.5 Task Actions (Done / Skipped)

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Mark task as done | 1. Click “Done” on a task.<br>2. Confirm action. | Task marked complete and removed from dashboard. | Passed |
| Mark task as skipped | 1. Click “Skip” on a task.<br>2. Confirm action. | Task marked skipped and removed from dashboard. | Passed |
| Undo not available | Attempt to undo action | No undo option (correct behaviour). | Passed |
| Task status updates in database | 1. Mark task done.<br>2. View task detail. | Status shows as completed. | Passed |

---

### 3.6 Link Integrity

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Click task row | Click any task row | Opens Task Detail page. | Passed |
| Bed link | Click bed name in dashboard table | Opens Bed Detail page. | Passed |
| Plant link | Click plant name in dashboard table | Opens Plant Detail page. | Passed |
| Task type link (if implemented) | Click type | Filters tasks by that type or opens type info (depending on implementation). | Passed |
| “View All Tasks” link | Click link | Navigates to full Tasks list. | Passed |

---

### 3.7 Layout and UI Behaviour

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Dashboard loads quickly | Log in and load dashboard | Page loads without delay. | Passed |
| Sections visually separated | View dashboard | Today, Upcoming, and Overdue sections clearly separated. | Passed |
| Overdue tasks visually highlighted | Create overdue task | Overdue tasks use distinct styling (e.g., red text). | Passed |
| Responsive layout | Resize window or test on mobile | Dashboard adapts to card layout on small screens. | Passed |
| Filters collapse on mobile | View dashboard on mobile | Filters collapse into a toggle panel. | Passed |
| No horizontal scrolling | View dashboard on mobile | Layout fits screen width. | Passed |

---

### 3.8 Error Handling

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Dashboard loads with no tasks | Remove all tasks | Dashboard shows empty-state message. | Passed |
| Dashboard loads with invalid filter params | Manually edit URL querystring | Dashboard falls back to default view without errors. | Passed |
| Attempt to access dashboard while logged out | Visit /dashboard | Redirect to login page. | Passed |

---

## 4. Beds

The Beds section allows users to create, view, update, and delete garden beds. It includes table sorting, search filtering, modal confirmations, and navigation links to related plants and tasks. This test suite validates all delivered functionality.

---

### 4.1 Viewing Beds

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Beds list loads | Navigate to **Beds** from navbar | Beds table displays all beds belonging to the logged‑in user | Passed |
| Beds sorted by default | Open Beds page | Default sort order is alphabetical by bed name | Passed |
| No beds created | Ensure user has no beds | Empty-state message displayed | Passed |
| Bed count accurate | Create multiple beds | All beds appear in list | Passed |

---

### 4.2 Creating Beds

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Create bed with valid data | 1. Click **Add Bed**.<br>2. Enter name and optional location.<br>3. Submit form. | Bed is created and appears in list | Passed |
| Create bed with missing name | 1. Click **Add Bed**.<br>2. Leave name blank.<br>3. Submit. | Field-level validation error shown | Passed |
| Create bed with duplicate name | 1. Create a bed named “Herbs”.<br>2. Attempt to create another “Herbs”. | Error shown (unique constraint enforced) | Passed |
| Cancel creation | 1. Click **Add Bed**.<br>2. Click **Cancel**. | User returned to Beds list with no changes | Passed |

---

### 4.3 Editing Beds

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Edit bed with valid data | 1. Click **Edit** on a bed.<br>2. Change name/location.<br>3. Submit. | Changes saved and reflected in list | Passed |
| Edit bed with invalid data | 1. Remove name.<br>2. Submit. | Validation error shown | Passed |
| Edit bed and cancel | 1. Click **Edit**.<br>2. Click **Cancel**. | No changes saved | Passed |
| Edit updates related pages | 1. Edit bed name.<br>2. Visit Plants/Tasks pages. | Updated bed name appears everywhere | x |

---

### 4.4 Deleting Beds

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Delete bed via modal | 1. Click **Delete**.<br>2. Confirm in modal. | Bed removed from list | Passed |
| Cancel delete | 1. Click **Delete**.<br>2. Click **Cancel**. | No deletion occurs | [issue-281](https://github.com/mrosevere/garden_timekeeper/issues/281) |
| Delete bed with related plants/tasks | 1. Create bed with plants/tasks.<br>2. Delete bed. | Bed deleted; related items handled per app logic (reassigned or cascaded) | Passed |
| Modal displays correct bed name | Open delete modal | Modal shows correct bed name for confirmation | Passed |

---

### 4.5 Sorting

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Sort by name | 1. Click **Name** column header.<br>2. Click again. | Ascending/descending toggle works | Passed |
| Sort by location | 1. Click **Location** header.<br>2. Toggle sort. | Beds sort alphabetically by location | Passed |
| Sort by created | 1. Click **Created** header.<br>2. Toggle sort. | Beds sort by date | Passed |

---

### 4.6 Filtering & Search

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Search by name | Enter text in search box | Only matching beds displayed | Passed |
| Search is case-insensitive | Search for lowercase/uppercase variations | Results identical | Passed |
| Filter by location | Select a location from dropdown | Only beds in that location shown | [Issue-282](https://github.com/mrosevere/garden_timekeeper/issues/282) |
| Clear filters | Apply filters then click **Reset** | Full bed list restored | Passed |

---

### 4.7 Link Integrity

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Bed name links to detail page | Click bed name | Opens Bed Detail page | Passed |
| “Add Plant” from bed list | Click **Add Bed** | Opens Bed creation form | Passed |
| “Edit from bed list | Click **Edit** | Opens task edit form with bed preselected | Passed |
| “Delete from bed list | Click **Delete** | Opens Delete Modal | Passed |

---

### 4.8 Layout & UI Behaviour

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Table layout consistent | View Beds list | Columns aligned, spacing consistent | Passed |
| Mobile layout | Resize to mobile width | Beds display as stacked cards | Passed |
| Filters collapse on mobile | View on small screen | Filters collapse into toggle panel | Passed |
| No horizontal scrolling | View on mobile | Layout fits screen width | Passed |
| Flash messages appear correctly | Create/edit/delete bed | Success/error messages displayed and styled correctly | Passed |

---

### 4.9 Error Handling & Permissions

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Access bed not owned by user | Change bed ID in URL | 404 or redirect (permission denied) | Passed |
| Invalid bed ID | Visit /beds/9999 | 404 page displayed | Passed |
| Server-side validation enforced | Submit manipulated form data | Invalid data rejected | Passed |
| Beds page while logged out | Visit /beds | Redirect to login | Passed |

---

## 5. Plants

The Plants section allows users to create, view, update, and delete plants associated with their garden beds. It includes rich‑text notes via Summernote, table sorting, search filtering, modal confirmations, and navigation links to related beds and tasks. This test suite validates all delivered functionality.

---

### 5.1 Viewing Plants

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Plants list loads | Navigate to **Plants** from navbar | Plants table displays all plants belonging to the logged‑in user | [issue-284](https://github.com/mrosevere/garden_timekeeper/issues/284) |
| Plants sorted by default | Open Plants page | Default sort order is alphabetical by plant name | Passed |
| No plants created | Ensure user has no plants | Empty-state message displayed | Passed |
| Plant count accurate | Create multiple plants | All plants appear in list | Passed |
| Bed names displayed | View Plants list | Each plant shows its associated bed | Passed |

---

### 5.2 Creating Plants

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Create plant with valid data | 1. Click **Add Plant**.<br>2. Enter name, select bed, optional notes.<br>3. Submit form. | Plant is created and appears in list | Passed |
| Create plant with missing name | 1. Click **Add Plant**.<br>2. Leave name blank.<br>3. Submit. | Field-level validation error shown | x |
| Create plant with missing bed | 1. Click **Add Plant**.<br>2. Do not select a bed.<br>3. Submit. | Validation error shown | x |
| Create plant with duplicate name in same bed | 1. Create “Tomatoes” in Bed A.<br>2. Attempt another “Tomatoes” in Bed A. | Error shown (unique constraint enforced per bed) | x |
| Create plant with same name in different bed | 1. Create “Tomatoes” in Bed A.<br>2. Create “Tomatoes” in Bed B. | Allowed (unique per bed, not global) | x |
| Cancel creation | 1. Click **Add Plant**.<br>2. Click **Cancel**. | User returned to Plants list with no changes | x |

---

### 5.3 Editing Plants

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Edit plant with valid data | 1. Click **Edit** on a plant.<br>2. Update name/bed/notes.<br>3. Submit. | Changes saved and reflected in list | x |
| Edit plant with invalid data | 1. Remove name.<br>2. Submit. | Validation error shown | x |
| Edit plant and cancel | 1. Click **Edit**.<br>2. Click **Cancel**. | No changes saved | x |
| Edit updates related pages | 1. Edit plant name.<br>2. Visit Tasks page. | Updated plant name appears everywhere | x |

---

### 5.4 Deleting Plants

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Delete plant via modal | 1. Click **Delete**.<br>2. Confirm in modal. | Plant removed from list | x |
| Cancel delete | 1. Click **Delete**.<br>2. Click **Cancel**. | No deletion occurs | x |
| Delete plant with related tasks | 1. Create tasks for a plant.<br>2. Delete plant. | Plant deleted; tasks handled per app logic (cascade or reassignment) | x |
| Modal displays correct plant name | Open delete modal | Modal shows correct plant name for confirmation | x |

---

### 5.5 Notes (Summernote)

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Add notes | 1. Create plant.<br>2. Enter formatted text in Summernote.<br>3. Save. | Notes saved and displayed correctly | x |
| Edit notes | 1. Open Edit Plant.<br>2. Modify notes.<br>3. Save. | Updated notes displayed | x |
| Rich text formatting preserved | Add headings, bold, lists | Formatting preserved on display | x |
| Invalid HTML sanitised | Paste invalid HTML | Sanitised safely by Summernote/Django | x |

---

### 5.6 Sorting

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Sort by name | 1. Click **Name** column header.<br>2. Click again. | Ascending/descending toggle works | x |
| Sort by bed | 1. Click **Bed** header.<br>2. Toggle sort. | Plants sort alphabetically by bed | x |
| Sort by date added (if implemented) | Click **Created** header | Sorts correctly | x |
| Sort persists after actions | 1. Sort by name.<br>2. Edit a plant.<br>3. Return to list. | Sort order remains applied | x |

---

### 5.7 Filtering & Search

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Search by name | Enter text in search box | Only matching plants displayed | x |
| Search is case-insensitive | Search for lowercase/uppercase variations | Results identical | x |
| Filter by bed | Select a bed from dropdown | Only plants in that bed shown | x |
| Clear filters | Apply filters then click **Clear** | Full plant list restored | x |

---

### 5.8 Link Integrity

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Plant name links to detail page | Click plant name | Opens Plant Detail page | x |
| Bed link | Click bed name in Plants list | Opens Bed Detail page | x |
| Tasks link from plant detail | On Plant Detail, click a task | Opens Task Detail page | x |
| “Add Task” from plant detail | Click **Add Task** | Opens task creation form with plant preselected | x |

---

### 5.9 Layout & UI Behaviour

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Table layout consistent | View Plants list | Columns aligned, spacing consistent | x |
| Mobile layout | Resize to mobile width | Plants display as stacked cards | x |
| Filters collapse on mobile | View on small screen | Filters collapse into toggle panel | x |
| No horizontal scrolling | View on mobile | Layout fits screen width | x |
| Flash messages appear correctly | Create/edit/delete plant | Success/error messages displayed and styled correctly | x |

---

### 5.10 Error Handling & Permissions

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Access plant not owned by user | Change plant ID in URL | 404 or redirect (permission denied) | x |
| Invalid plant ID | Visit /plants/9999 | 404 page displayed | x |
| Server-side validation enforced | Submit manipulated form data | Invalid data rejected | x |
| Plants page while logged out | Visit /plants | Redirect to login | X |

---
