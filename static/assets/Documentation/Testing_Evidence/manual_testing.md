# Manual Testing Documentation

This document outlines the complete manual testing performed for the **Garden Timekeeper** application. All tests were carried out on both the deployed Heroku version and the local development environment. Testing covers all major features, negative scenarios, validation behaviour, responsiveness, accessibility, and deployment reliability.

# Table of Contents

- [How to Use This Document](#how-to-use-this-document)
- [Mapping to README Testing Summary](#mapping-to-readme-testing-summary)

## 1. Authentication
- [1.1 Registration](#11-registration)
- [1.2 Login](#12-login)
- [1.3 Logout](#13-logout)
- [1.4 Password Reset (Forgot Password)](#14-password-reset-forgot-password)
- [1.5 Password Change (Logged-In Users)](#15-password-change-logged-in-users)
- [1.6 Account Page (Profile)](#16-account-page-profile)
- [1.7 Access Control & Permissions](#17-access-control--permissions)
- [1.8 Session & Cookie Behaviour](#18-session--cookie-behaviour)
- [1.9 Usability & UX](#19-usability--ux)

## 2. Navigation & Layout
- [2.1 Navbar Behaviour](#21-navbar-behaviour)
- [2.2 Footer](#22-footer)
- [2.3 Layout Consistency](#23-layout-consistency)
- [2.4 Navigation Error Handling](#24-navigation-error-handling)
- [2.5 Internal Link Integrity](#25-internal-link-integrity)
- [2.6 Responsive Navigation Layout](#26-responsive-navigation-layout)

## 3. Dashboard
- [3.1 Display of Due, Upcoming, and Overdue Tasks](#31-display-of-due-upcoming-and-overdue-tasks)
- [3.2 Filtering](#32-filtering)
- [3.3 Sorting](#33-sorting)
- [3.4 Pagination and Month Navigation](#34-pagination-and-month-navigation-if-applicable)
- [3.5 Task Actions (Done / Skipped)](#35-task-actions-done--skipped)
- [3.6 Link Integrity](#36-link-integrity)
- [3.7 Layout and UI Behaviour](#37-layout-and-ui-behaviour)
- [3.8 Error Handling](#38-error-handling)

## 4. Beds
- [4.1 Viewing Beds](#41-viewing-beds)
- [4.2 Creating Beds](#42-creating-beds)
- [4.3 Editing Beds](#43-editing-beds)
- [4.4 Deleting Beds](#44-deleting-beds)
- [4.5 Sorting](#45-sorting)
- [4.6 Filtering & Search](#46-filtering--search)
- [4.7 Link Integrity](#47-link-integrity)
- [4.8 Layout & UI Behaviour](#48-layout--ui-behaviour)
- [4.9 Error Handling & Permissions](#49-error-handling--permissions)

## 5. Plants
- [5.1 Viewing Plants](#51-viewing-plants)
- [5.2 Creating Plants](#52-creating-plants)
- [5.3 Editing Plants](#53-editing-plants)
- [5.4 Deleting Plants](#54-deleting-plants)
- [5.5 Notes (Summernote)](#55-notes-summernote)
- [5.6 Sorting](#56-sorting)
- [5.7 Filtering & Search](#57-filtering--search)
- [5.8 Link Integrity](#58-link-integrity)
- [5.9 Layout & UI Behaviour](#59-layout--ui-behaviour)
- [5.10 Error Handling & Permissions](#510-error-handling--permissions)

## 6. Tasks
- [6.1 Viewing Tasks](#61-viewing-tasks)
- [6.2 Creating Tasks](#62-creating-tasks)
- [6.3 Editing Tasks](#63-editing-tasks)
- [6.4 Deleting Tasks](#64-deleting-tasks)
- [6.5 Marking Tasks as Done or Skipped](#65-marking-tasks-as-done-or-skipped)
- [6.6 Sorting](#66-sorting)
- [6.7 Filtering & Search](#67-filtering--search)
- [6.8 Link Integrity](#68-link-integrity)
- [6.9 Layout & UI Behaviour](#69-layout--ui-behaviour)
- [6.10 Error Handling & Permissions](#610-error-handling--permissions)
- [6.11 Task Scheduling (Create Task Page)](#611-task-scheduling-create-task-page)
  - [6.11.1 All‑Year Toggle](#6111-allyear-toggle)
  - [6.11.2 Seasonal Start/End Month](#6112-seasonal-startend-month)
  - [6.11.3 Frequency Field](#6113-frequency-field)
  - [6.11.4 Repeat Interval Field](#6114-repeat-interval-field)
  - [6.11.5 Notes Field (Interaction With Scheduling)](#6115-notes-field-interaction-with-scheduling)
  - [6.11.6 Combined Scheduling Logic](#6116-combined-scheduling-logic)
  - [6.11.7 Form Validation & Error Handling](#6117-form-validation--error-handling)
  - [6.11.8 UI Behaviour](#6118-ui-behaviour)

## 7. User Flow Testing
- [7.1 Registration → Login → Dashboard Access](#71-registration--login--dashboard-access)
- [7.2 Create Bed → Create Plant → Create Task](#72-create-bed--create-plant--create-task)
- [7.3 Edit Flow (Bed → Plant → Task)](#73-edit-flow-bed--plant--task)
- [7.4 Delete Flow (Task → Plant → Bed)](#74-delete-flow-task--plant--bed)
- [7.5 Dashboard → Task Completion Flow](#75-dashboard--task-completion-flow)
- [7.6 Permissions Flow (User A vs User B)](#76-permissions-flow-user-a-vs-user-b)
- [7.7 Error & Redirect Flow](#77-error--redirect-flow)
- [7.8 Logout Flow](#78-logout-flow)

## 8. Cross‑Browser Testing
- [8.1 Page Rendering & Layout Consistency](#81-page-rendering--layout-consistency)
- [8.2 Form Behaviour & Validation](#82-form-behaviour--validation)
- [8.3 Navigation & Interaction](#83-navigation--interaction)
- [8.4 Dashboard Behaviour](#84-dashboard-behaviour)
- [8.5 Performance & Stability](#85-performance--stability)
- [8.6 Known Cross‑Browser Issues](#86-known-crossbrowser-issues)

## 9. Accessibility & Performance Testing
- [9.1 Accessibility Testing (WAVE & Manual Checks)](#91-accessibility-testing-wave--manual-checks)
- [9.2 Lighthouse Accessibility Audit](#92-lighthouse-accessibility-audit)
- [9.3 Performance Testing (Lighthouse)](#93-performance-testing-lighthouse)
- [9.4 Best Practices & SEO (Lighthouse)](#94-best-practices--seo-lighthouse)
- [9.5 Manual Performance Checks](#95-manual-performance-checks)
- [9.6 Known Accessibility or Performance Issues](#96-known-accessibility-or-performance-issues)

## 10. Additional Validation Evidence
- [Additional Validation Evidence](#10-additional-validation-evidence)

## How to Use This Document

This document contains the full manual testing evidence for the Garden Timekeeper application.  
It is organised by **feature area** (Authentication, Navigation, Dashboard, Beds, Plants, Tasks) so that each component can be reviewed independently.

The README provides a high‑level summary of the testing approach.  
This document provides the **detailed test cases, results, and issue references**.

---

## Mapping to README Testing Summary

The following table shows how the README testing categories map to the sections in this document:

| README Category | Evidence in This Document |
|-----------------|---------------------------|
| **Functional Testing** | Dashboard, Beds, Plants, Tasks, Navigation |
| **Form & Validation Testing** | All Create/Edit forms across Beds, Plants, Tasks, Authentication |
| **Responsive & Cross‑Browser Testing** | Navigation & Layout → Responsive Layout, plus each feature’s Layout section |
| **User Flow Testing** | Authentication → Navigation → CRUD flows in Beds/Plants/Tasks |
| **Permissions Testing** | Authentication → Access Control & Permissions |
| **Error Handling** | Each feature’s Error Handling section |
| **Scheduling Logic** | Tasks → Recurring Task Logic (if included) |

This mapping makes it easy for assessors to verify that **every requirement in the README has corresponding evidence** in the manual testing document.


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
| Edit updates related pages | 1. Edit bed name.<br>2. Visit Plants/Tasks pages. | Updated bed name appears everywhere | Passed |

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
| Create plant with missing name | 1. Click **Add Plant**.<br>2. Leave name blank.<br>3. Submit. | Field-level validation error shown | [issue-286](https://github.com/mrosevere/garden_timekeeper/issues/286) |
| Create plant with missing type | 1. Click **Add Plant**.<br>2. Do not select a type.<br>3. Submit. | Validation error shown | Passed |
| Create plant with duplicate name | 1. Create “Tomatoes” in Bed A.<br>2. Attempt another “Tomatoes” in Bed A. | Multiple plants per bed are permitted  | Passed |
| Create plant with same name in different bed | 1. Create “Tomatoes” in Bed A.<br>2. Create “Tomatoes” in Bed B. | Allowed (unique per bed is NOT enforced) | Passed |
| Cancel creation | 1. Click **Add Plant**.<br>2. Click **Cancel**. | User returned to Plants list with no changes | Passed |

---

### 5.3 Editing Plants

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Edit plant with valid data | 1. Click **Edit** on a plant.<br>2. Update name/bed/notes.<br>3. Submit. | Changes saved and reflected in list | Passed |
| Edit plant with invalid data | 1. Remove name.<br>2. Submit. | Validation error shown | Passed |
| Edit plant and cancel | 1. Click **Edit**.<br>2. Click **Cancel**. | No changes saved | Passed |
| Edit updates related pages | 1. Edit plant name.<br>2. Visit Tasks page. | Updated plant name appears everywhere | Passed |

---

### 5.4 Deleting Plants

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Delete plant via modal | 1. Click **Delete**.<br>2. Confirm in modal. | Plant removed from list | Passed |
| Cancel delete | 1. Click **Delete**.<br>2. Click **Cancel**. | No deletion occurs | Passed |
| Delete plant with related tasks | 1. Create tasks for a plant.<br>2. Delete plant. | Plant deleted; tasks handled per app logic (cascade or reassignment) | Passed |
| Modal displays correct plant name | Open delete modal | Modal shows correct plant name for confirmation | Passed |

---

### 5.5 Notes (Summernote)

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Add notes | 1. Create plant.<br>2. Enter formatted text in Summernote.<br>3. Save. | Notes saved and displayed correctly | [issue-290](https://github.com/mrosevere/garden_timekeeper/issues/290) |
| Edit notes | 1. Open Edit Plant.<br>2. Modify notes.<br>3. Save. | Updated notes displayed | [issue-290](https://github.com/mrosevere/garden_timekeeper/issues/290) |
| Rich text formatting preserved | Add headings, bold, lists | Formatting preserved on display | Passed |
| Invalid HTML sanitised | Paste invalid HTML | Sanitised safely by Summernote/Django | Passed |

---

### 5.6 Sorting

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Sort by name | 1. Click **Name** column header.<br>2. Click again. | Ascending/descending toggle works | Passed |
| Sort by bed | 1. Click **Bed** header.<br>2. Toggle sort. | Plants sort alphabetically by bed | Passed |
| Sort by date added (if implemented) | Click **Created** header | Sorts correctly | Passed |

---

### 5.7 Filtering & Search

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Search by name | Enter text in search box | Only matching plants displayed | Passed |
| Search is case-insensitive | Search for lowercase/uppercase variations | Results identical | Passed |
| Filter by bed | Select a bed from dropdown | Only plants in that bed shown | Passed |
| Filter by lifespan | Select a lifespan from dropdown | Only plants with that lifespan shown | Passed |
| Filter by type | Select a type from dropdown | Only plants with that type shown | Passed |
| Clear filters | Apply filters then click **Clear** | Full plant list restored | Passed |

---

### 5.8 Link Integrity

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Plant name links to detail page | Click plant name | Opens Plant Detail page | Passed |
| Bed link | Click bed name in Plants list | Opens Bed Detail page | [issue-291](https://github.com/mrosevere/garden_timekeeper/issues/291) |
| Tasks link from plant detail | On Plant Detail, click a task | Opens Task Detail page | Passed |
| “Add Task” from plant detail | Click **Add Task** | Opens task creation form with plant preselected | Passed |

---

### 5.9 Layout & UI Behaviour

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Table layout consistent | View Plants list | Columns aligned, spacing consistent | Passed |
| Mobile layout | Resize to mobile width | Plants display as stacked cards | Passed |
| Filters collapse on mobile | View on small screen | Filters collapse into toggle panel | Passed |
| No horizontal scrolling | View on mobile | Layout fits screen width | Passed |
| Flash messages appear correctly | Create/edit/delete plant | Success/error messages displayed and styled correctly | Passed |

---

### 5.10 Error Handling & Permissions

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Access plant not owned by user | Change plant ID in URL | 404 or redirect (permission denied) | Passed |
| Invalid plant ID | Visit /plants/9999 | 404 page displayed | Passed |
| Server-side validation enforced | Submit manipulated form data | Invalid data rejected | Passed |
| Plants page while logged out | Visit /plants | Redirect to login | Passed |

---

## 6. Tasks

The Tasks section allows users to create, view, update, complete, skip, and delete tasks associated with plants and beds. It includes recurring task logic, table sorting, search filtering, modal confirmations, and navigation links to related beds and plants. This test suite validates all delivered functionality.

---

### 6.1 Viewing Tasks

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Tasks list loads | Navigate to **Plant List -> Plant Details** | Tasks table displays all tasks belonging to the logged‑in user and the selected plant | Passed |
| Tasks sorted by default | Open Plant Details page | Default sort order is by due date ascending | Passed |
| No tasks created | Ensure user has no tasks | Empty-state message displayed | Passed |
| Task count accurate | Create multiple tasks | All tasks appear in list | Passed |
| Table fields displayed in Task List | View Plant Details -> Task list | Each task shows its associated Next Due date, Status, Season and Frequency | Passed |

---

### 6.2 Creating Tasks

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Create task with valid data | 1. Click **Add Task**.<br>2. Enter name, Notes and Task Scheduling.<br>3. Submit form. | Task is created and appears in list | Passed |
| Create task with missing name | Leave name blank and submit | validation error shown | Passed |
| Cancel creation | Click **Cancel** on Add Task form | User returned to Tasks list with no changes | Passed |

---

### 6.3 Editing Tasks

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Edit task with valid data | 1. Click **Edit**.<br>2. Update fields.<br>3. Submit. | Changes saved and reflected in list | Passed |
| Edit task with invalid data | Remove required fields and submit | Validation error shown | Passed |
| Edit recurring task | Change recurrence settings | Updated recurrence applied to future tasks | Passed |
| Edit and cancel | Click **Cancel** on edit form | No changes saved | Passed |
| Edit updates related pages | Edit task name or date | Updated values appear on Dashboard and detail pages | Passed |

---

### 6.4 Deleting Tasks

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Delete task via modal | 1. Click **Delete**.<br>2. Confirm in modal. | Task removed from list | Passed |
| Cancel delete | 1. Click **Delete**.<br>2. Click **Cancel**. | No deletion occurs | Passed |
| Delete recurring task | Delete a recurring task | Only selected instance deleted (depending on implementation) | Passed |
| Modal displays correct task name | Open delete modal | Modal shows correct task name for confirmation | Passed |

---

### 6.5 Marking Tasks as Done or Skipped

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Mark task as done | Click **Done** on a task | Task marked complete and removed from active lists | Passed |
| Mark task as skipped | Click **Skip** on a task | Task marked skipped and removed from active lists | Passed |
| Recurring task completion | Mark recurring task as done | Next occurrence generated automatically | Passed |
| Recurring task completion | Mark recurring task as skip | Next occurrence generated automatically | Passed |

---

### 6.6 Sorting

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Sort by name | Click **Task Name** header | Tasks sort alphabetically | Passed |
| Sort by due date | Click **Next Date** header | Ascending/descending toggle works | Passed |
| Sort by bed | Click **Status** header | Tasks sort alphabetically by status | Passed |
| Sort by plant | Click **Season** header | Tasks sort alphabetically by season | Passed |
| Sort by type | Click **Frequency** header | Tasks sort alphabetically by Frequency | Passed |

---

### 6.7 Filtering & Search

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Search by task name | Enter text in search box | Only matching tasks displayed | Passed |
| Search is case-insensitive | Search using different casing | Results identical | Passed |
| Filter by Status | Select a Status from dropdown | Only tasks with that status shown | Passed |
| Filter by Season | Select "In Season" from dropdown | Only tasks for that are in season are shown | Passed |
| Filter by Season | Select "Out of Season" from dropdown | Only tasks for that are out of season are shown | Passed | 
| Clear filters | Remove any filters | Full task list restored | Passed |
| No results | Search for a task name that doesn't exist | No results display | Passed |

---

### 6.8 Link Integrity

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Task name links to detail page | Click task name | Opens Task Detail page | Passed |
| “Edit Task” from plant detail | Click **Edit** Task on Plant Detail | Opens task edit form | Passed |
| “Delete Task” from plant detail | Click **Delete** Task on Plant Detail | Opens task deletion modal | Passed |

---

### 6.9 Layout & UI Behaviour

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Table layout consistent | View Tasks list | Columns aligned, spacing consistent | Passed |
| Mobile layout | Resize to mobile width | Tasks display as stacked cards | Passed |
| Filters collapse on mobile | View on small screen | Filters collapse into toggle panel | x |
| No horizontal scrolling | View on mobile | Layout fits screen width | Passed |
| Flash messages appear correctly | Create/edit/delete task | Success/error messages displayed and styled correctly | Passed |

---

### 6.10 Error Handling & Permissions

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Access task not owned by user | Change task ID in URL | 404 or redirect (permission denied) | Passed |
| Invalid task ID | Visit /tasks/9999 | 404 page displayed | Passed |
| Server-side validation enforced | Submit manipulated form data | Invalid data rejected | Passed |
| Tasks page while logged out | Visit /tasks | Redirect to login | Passed |

---

## 6.11 Task Scheduling (Create Task Page)

The Task Scheduling section controls when a task occurs throughout the year, including seasonal ranges, all‑year tasks, frequency, and repeat intervals. This suite validates all delivered scheduling functionality and form behaviour.

---

### 6.11.1 All‑Year Toggle

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Enable “All Year” | 1. Open Create Task.<br>2. Tick **All Year** checkbox.<br>3. Submit form. | Task saved with all‑year scheduling; seasonal fields ignored. | Passed |
| Disable “All Year” | 1. Untick **All Year**.<br>2. Submit form with seasonal months. | Seasonal start/end months required and validated. | Passed |
| All‑Year + Seasonal window | 1. Tick **All Year**.<br>2. Select Seasonal Start month.<br>3. Select Seasonal End month. | All Year checkbox is unticked. | Passed |
| All‑Year + frequency | 1. Tick **All Year**.<br>2. Select frequency (e.g., Weekly).<br>3. Submit. | Frequency applied across entire year. | Passed |

---

### 6.11.2 Seasonal Start/End Month

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Valid seasonal range | 1. Untick **All Year**.<br>2. Select Start = March, End = October.<br>3. Submit. | Task saved with seasonal window. | Passed |
| Missing start month | 1. Untick **All Year**.<br>2. Leave start month blank.<br>3. Submit. | User cannot deselect a start month. | Passed |
| Missing end month | 1. Untick **All Year**.<br>2. Leave end month blank.<br>3. Submit. | User cannot deselect a start month. | Passed |
| Start month after end month | 1. Start = October.<br>2. End = March.<br>3. Submit. | Validation error: start must be before end. | Passed |
| Seasonal range + frequency | 1. Select seasonal months.<br>2. Choose frequency (e.g., Monthly).<br>3. Submit. | Frequency applied only within seasonal window. | Passed |
| Seasonal range + repeat | 1. Select seasonal months.<br>2. Set repeat interval (e.g., every 2 weeks).<br>3. Submit. | Repeat interval applied within seasonal window. | Passed |

---

### 6.11.3 Frequency Field

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Select Weekly | Choose **Weekly** frequency | Task is scheduled weekly within the seasonal window | Passed |
| Select Monthly | Choose **Monthly** frequency | Task is scheduled Monthly within the seasonal window | Passed |
| Select Monthly | Choose **Quarterly** frequency | Task is scheduled Quarterly within the seasonal window | Passed |
| Select Monthly | Choose **Half Yearly** frequency | Task is scheduled Half Yearly within the seasonal window | Passed |
| Select Yearly | Choose **Yearly** frequency | Task is scheduled Yearly within the seasonal window | Passed |
| Frequency required | Leave frequency blank and submit | User cannot deselect a frequency | Passed |
| Frequency + All Year | Tick All Year + choose frequency | Task scheduled across full year | Passed |
| Frequency + Seasonal | Select seasonal months + frequency | Task scheduled only within seasonal window | Passed |
| Frequency + Repeat deselected | Select seasonal months + deselect Repeat | Task scheduled as a ONCE ONLY and does not reoccur | Passed |

---

### 6.11.4 Repeat Interval Field

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Repeat Enabled | Select frequency + repeat (e.g., Weekly) | Task displays on the dashboard weekly during seasonal window | Passed |
| Repeat Disabled | Select frequency + DISABLE repeat (e.g., Weekly) | Task displays on the dashboard ONCE | Passed |
| Repeat interval updates dynamically | Change frequency | Repeat options update to match frequency | Passed |
| Repeat interval + seasonal | Select seasonal months + repeat | Repeat applied only within seasonal window | Passed |

---

### 6.11.5 Notes Field (Interaction With Scheduling)

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Notes saved with scheduling | Enter notes + scheduling fields | Notes saved correctly | Passed |
| Notes validation independent | Leave notes blank | Scheduling still validated normally | Passed |
| Notes formatting preserved | Enter formatted text | Formatting preserved on save | Passed |

---

### 6.11.6 Combined Scheduling Logic

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| All Year + Weekly + Repeat | Tick All Year + Weekly + Repeat every 1 week | Task repeats weekly all year | Passed |
| Seasonal + Weekly + Repeat | Seasonal months + Weekly + Repeat every 2 weeks | Task repeats every 2 weeks within seasonal window | Passed |
| Seasonal + Monthly + Repeat | Seasonal months + Monthly + Repeat every 1 month | Task repeats monthly within seasonal window | Passed |
| Seasonal + Yearly | Seasonal months + Yearly | Task occurs once per year within seasonal window | Passed |
| All Year + Yearly | Tick All Year + Yearly | Task occurs once per year | Passed |

---

### 6.11.7 Form Validation & Error Handling

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| HTML5 validation disabled | Inspect form tag (`novalidate`) | Browser does not block submission; Django handles errors | Passed |
| Server‑side validation enforced | Manipulate POST data (e.g., invalid month) | Server rejects invalid values | Passed |
| Error summary displayed | Submit invalid form | “Please correct the errors below.” alert shown | Passed |
| Field‑level errors displayed | Submit invalid form | Errors appear under each invalid field | Passed |

---

### 6.11.8 UI Behaviour

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Scheduling card collapses correctly | View on mobile | Card layout adapts to mobile width | Passed |
| Frequency and repeat aligned | View form | Fields aligned in two‑column layout | Passed |
| Cancel button returns to plant | Click **Cancel** | Redirects to Plant Detail page | Passed |
| Delete button visible only when editing | Open Create Task | Delete button not shown | Passed |

---

## 7. User Flow Testing

This section validates full end‑to‑end user journeys across the Garden Timekeeper application.  
Unlike feature‑specific tests, these flows ensure that the system behaves correctly when users perform multi‑step actions that span multiple pages, models, and permissions.

User flow testing confirms:
- Navigation between features works intuitively  
- Redirects behave correctly  
- Success/error messages appear at the right time  
- CRUD operations work in sequence  
- Users cannot break flows by skipping steps or manipulating URLs  

---

### 7.1 Registration → Login → Dashboard Access

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| New user onboarding | 1. Register a new account.<br>2. Log in with the new credentials.<br>3. Arrive on Home Page.<br>4. Create a Bed.<br>5. From the **Success** message, add a plant.br>6. From the **Success** message, add a task. | User successfully registers, logs in, and is redirected to Home page, where they can follow the flow to create a Bed, Plant and Task. | Passed |
| Login redirect behaviour | 1. Attempt to access /beds while logged out.<br>2. System redirects to login.<br>3. After login, user is redirected back to /beds. | Redirect chain works correctly. | Passed |

---

### 7.2 Create Bed → Create Plant → Create Task

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Full content creation flow | 1. From Bed List, create a new Bed.<br>2. From Plant List, click **Add Plant**.<br>3. Create a Plant.<br>4. From Plant Detail, click **Add Task**.<br>5. Create a Task. | Bed, Plant, and Task created successfully and linked correctly. | Passed |
| Success messages appear | Perform each create action | Success messages appear after each creation. | Passed |

---

### 7.3 Edit Flow (Bed → Plant → Task)

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Edit all related objects | 1. Edit a Bed name.<br>2. Edit a Plant name.<br>3. Edit a Task name/date/type.<br>4. Return to Dashboard. | All edits persist and appear correctly across all pages. | Passed |
| Edited names propagate | 1. Edit Bed name.<br>2. View Plants and Tasks lists. | Updated Bed name appears everywhere. | Passed |
| Cancel edit | 1. Open Edit form.<br>2. Click Cancel. | No changes saved; user returned to previous page. | Passed |

---

### 7.4 Delete Flow (Task → Plant → Bed)

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Delete task from detail page | 1. Open Task Detail.<br>2. Click Delete.<br>3. Confirm. | Task removed; user redirected to Plant Detail. | Passed |
| Delete plant with tasks | 1. Create Plant with tasks.<br>2. Delete Plant.<br>3. Confirm. | Plant deleted; tasks handled per app logic (cascade). | Passed |
| Delete bed with plants | 1. Create Bed with Plants.<br>2. Delete Bed.<br>3. Confirm. | Bed deleted; plants handled per app logic (plant unassigned). | Passed |

---

### 7.5 Dashboard → Task Completion Flow

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Mark task as done | 1. From Dashboard, click Done on a task.<br>2. Confirm action. | Task disappears from Dashboard and shows as completed in Task Detail. | Passed |
| Mark task as skipped | 1. From Dashboard, click Skip.<br>2. Confirm action. | Task disappears from Dashboard and shows as skipped. | Passed |
| Dashboard updates immediately | Complete or skip a task | Dashboard refreshes and no longer shows the task. | Passed |

---

### 7.6 Permissions Flow (User A vs User B)

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| User A cannot access User B’s content | 1. Log in as User A.<br>2. Attempt to access User B’s Bed/Plant/Task via URL. | 404 or redirect to Dashboard. | Passed |
| User B cannot edit User A’s content | 1. Log in as User B.<br>2. Attempt to access edit URLs for User A’s objects. | Access denied (404 or redirect). | Passed |
| Cross‑user dashboard protection | Log in as User B and attempt /dashboard?user=A | Dashboard only shows User B’s tasks. | Passed |

---

### 6.7 Error & Redirect Flow

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Invalid object ID | Visit /plants/9999 or /beds/9999 | Custom 404 page displayed. | Passed |
| Form submission with errors | Submit form with missing required fields | Error messages displayed; form retains entered data. | Passed |
| Cancel buttons behave correctly | Click Cancel on any form | User returned to correct parent page. | Passed |

---

### 7.8 Logout Flow

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Logout from any page | 1. Log in.<br>2. Navigate to any page.<br>3. Click Logout. | User logged out and redirected to Login page. | Passed |
| Access after logout | Attempt to access /beds, /plants, /tasks after logout | Redirect to Login page. | Passed |

## 8. Cross‑Browser Testing

Cross‑browser testing verifies that the Garden Timekeeper application behaves consistently across different browsers, rendering engines, and device types.  
Testing was performed on both desktop and mobile versions of:

- **Google Chrome (latest)**
- **Mozilla Firefox (latest)**
- **Safari (iOS)**
- **Microsoft Edge (latest)**

The goal was to ensure consistent layout, navigation, form behaviour, and interactive elements across all supported environments.

---

### 8.1 Page Rendering & Layout Consistency

| Test | Steps | Expected Result | Chrome | Firefox | Safari | Edge |
|------|--------|-----------------|--------|---------|--------|------|
| Homepage loads correctly | Open homepage | Layout renders correctly with no visual defects | x | x | x | x |
| Navbar layout consistent | View navbar on each browser | Navbar items aligned and visible | x | x | x | x |
| Footer layout consistent | Scroll to bottom | Footer sticks to bottom and does not overlap content | x | x | x | x |
| Dashboard layout | Open Dashboard | Cards/tables render correctly with no overflow | x | x | x | x |
| Tables render correctly | Open Beds/Plants/Tasks lists | Columns aligned, no clipping | x | x | x | x |
| Mobile responsive layout | Resize window or test on mobile | Layout switches to stacked/mobile view | x | x | x | x |

---

### 8.2 Form Behaviour & Validation

| Test | Steps | Expected Result | Chrome | Firefox | Safari | Edge |
|------|--------|-----------------|--------|---------|--------|------|
| Form fields render correctly | Open any Create/Edit form | All fields visible and styled correctly | Pass | Pass | Pass | Pass |
| Client‑side validation disabled | Inspect form (`novalidate`) | Browser does not block submission | Pass | Pass | Pass | Pass |
| Django validation messages appear | Submit invalid form | Error messages appear under fields | Pass | Pass | Pass | Pass |
| Date picker behaviour | Use date fields | Date input works consistently | Pass | Pass | Pass | Pass |
| Summernote editor loads | Open Plant Create/Edit | Editor loads and toolbar works | Pass | Pass | Pass | Pass |

---

### 8.3 Navigation & Interaction

| Test | Steps | Expected Result | Chrome | Firefox | Safari | Edge |
|------|--------|-----------------|--------|---------|--------|------|
| Navbar links work | Click each navbar item | Correct pages load | Pass | Pass | Pass | Pass |
| Hamburger menu works | Test on mobile | Menu opens/closes correctly | Pass | Pass | Pass | Pass |
| Delete modals open | Click Delete on any item | Modal opens and buttons work | Pass | Pass | Pass | Pass |
| Sorting works | Click table headers | Sorting toggles correctly | Pass | Pass | Pass | Pass |
| Filtering works | Apply filters | Results update correctly | Pass | Pass | Pass | Pass |

---

### 8.4 Dashboard Behaviour

| Test | Steps | Expected Result | Chrome | Firefox | Safari | Edge |
|------|--------|-----------------|--------|---------|--------|------|
| Tasks grouped correctly | Open Dashboard | Due / Overdue / Upcoming sections display correctly | Pass | Pass | Pass | Pass |
| Mark task as done | Click Done | Task disappears and updates status | Pass | Pass | Pass | Pass |
| Mark task as skipped | Click Skip | Task disappears and updates status | Pass | Pass | Pass | Pass |
| Filters work | Apply filters | Dashboard updates correctly | Pass | Pass | Pass | Pass |

---

### 8.5 Performance & Stability

| Test | Steps | Expected Result | Chrome | Firefox | Safari | Edge |
|------|--------|-----------------|--------|---------|--------|------|
| Page load speed acceptable | Load Dashboard, Beds, Plants | Pages load without noticeable delay | Pass | Pass | Pass | Pass |
| No console errors | Open DevTools console | No JavaScript errors | Pass | Pass | Pass | Pass |
| No layout shift on load | Refresh pages | Layout stable with no jumping | Pass | Pass | Pass | Pass |

---

### 8.6 Known Cross‑Browser Issues

| Issue | Browser | Description | Status |
|-------|----------|-------------|--------|
| None identified | All | No cross‑browser inconsistencies were found during testing. | Passed |

---

## 9. Accessibility & Performance Testing

Accessibility and performance testing ensures that the Garden Timekeeper application is usable by all users, loads efficiently, and follows modern best practices.  
Testing was carried out using automated tools (WAVE, Lighthouse), browser DevTools, and manual keyboard‑only navigation checks.

---

### 9.1 Accessibility Testing (WAVE & Manual Checks)

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Colour contrast | Inspect text/background combinations | All text meets WCAG AA contrast ratios | Passed |
| Alt text on images | Inspect all images (including Cloudinary uploads) | All non‑decorative images have descriptive alt text | Passed |
| Form label association | Inspect form fields | All inputs have associated `<label>` elements | Passed |
| ARIA roles | Inspect navigation, modals, and interactive elements | ARIA roles applied correctly where needed | Passed |
| Keyboard navigation | Navigate entire site using Tab/Shift+Tab | All interactive elements reachable in logical order | Passed |
| Focus visibility | Tab through forms and navigation | Visible focus outline present on all elements | Passed |
| Modal accessibility | Open delete confirmation modals | Focus trapped inside modal; Escape closes modal | Passed |
| Error message accessibility | Submit invalid forms | Errors announced visually and positioned near fields | Passed |

**NOTE** WAVE generated warnings for "Skipped heading level" even when the HTML was valid;
For example:
```
    <h1 class="mb-4 h2">Login</h1>
```
- It is an &lt;h1> element, but set to display as &lt;h2>
- WAVE considers this a skipped heading level still.

<br>

---

### 9.2 Lighthouse Accessibility Audit

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Lighthouse accessibility score | Run Lighthouse on Dashboard, Beds, Plants, Tasks | Score ≥ 90 on all tested pages | Passed |
| ARIA validation | Review Lighthouse report | No ARIA misuse or missing attributes | Passed |
| Heading structure | Inspect page headings | Logical `<h1> → h2 → h3>` hierarchy | Passed |
| Link purpose | Inspect all links | Links have meaningful text (no “click here”) | Passed |

See [Lighthouse_validation.md](/static/assets/Documentation/Testing_Evidence/Lighthouse_validation.md)

<br>

---

### 9.3 Performance Testing (Lighthouse)

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Lighthouse performance score | Run Lighthouse on key pages | Score ≥ 80 on all tested pages | x |
| Image optimisation | Inspect Cloudinary‑served images | Images served in modern formats (WebP/auto) | x |
| Caching behaviour | Inspect network tab | Static assets cached effectively | x |
| JavaScript execution | Review Lighthouse report | No long‑running scripts; minimal blocking time | x |
| CSS efficiency | Inspect CSS | No excessive unused CSS; styles load quickly | x |

See [Lighthouse_validation.md](/static/assets/Documentation/Testing_Evidence/Lighthouse_validation.md)

<br>

---

### 9.4 Best Practices & SEO (Lighthouse)

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Lighthouse best‑practice score | Run Lighthouse | Score ≥ 90 | x |
| HTTPS enforcement | Inspect site URL | All pages served over HTTPS | x |
| Mixed content | Inspect console | No mixed‑content warnings | x |
| SEO score | Run Lighthouse SEO audit | Score ≥ 90 | x |
| Meta tags | Inspect `<head>` | Title, description, viewport meta present | x |

<br>

See [Lighthouse_validation.md](/static/assets/Documentation/Testing_Evidence/Lighthouse_validation.md)

---

### 9.5 Manual Performance Checks

| Test | Steps | Expected Result | Status |
|------|--------|-----------------|--------|
| Page load speed | Load Dashboard, Beds, Plants, Tasks | Pages load within acceptable time | x |
| No layout shift | Refresh pages | No CLS (Cumulative Layout Shift) issues | x |
| Smooth navigation | Navigate between pages | No noticeable lag or stutter | x |
| Modal performance | Open/close modals repeatedly | Modals open instantly with no delay | x |
| Form submission speed | Submit forms | Server responds promptly; no timeouts | x |

<br>

---

### 9.6 Known Accessibility or Performance Issues

| Issue | Description | Status |
|-------|-------------|--------|
| None identified | No accessibility or performance issues were found during testing. | Passed |

<br>

---

## 10. Additional Validation Evidence

The README references several standalone validation documents that provide full evidence for code‑quality checks.  
To ensure assessors can easily locate all required validation artefacts, the documents are linked here as well.

These documents are stored in the repository alongside this manual testing file.

| Validation Area | Document | Description |
|-----------------|----------|-------------|
| **HTML Validation** | [html_validation.md](/static/assets/Documentation/Testing_Evidence/HTML_Validation_final_run.md) | Full W3C validation results for all templates, including resolved issues and links to GitHub issues. |
| **CSS Validation** | [css_validation.md](/static/assets/Documentation/Testing_Evidence/CSS_validation.md) | Results from W3C CSS Validator for all custom stylesheets, including warnings and fixes. |
| **JavaScript Validation** | [javascript_validation.md](/static/assets/Documentation/Testing_Evidence/JavaScript_validation.md) | JSHint validation results for custom JS, with notes on third‑party libraries. |
| **Python Validation** | [python_validation.md](/static/assets/Documentation/Testing_Evidence/Python_validation.md) | flake8, black, and Django system check results, including any resolved linting issues. |
| **Defect Report** | [Bug_list.md](/static/assets/Documentation/Testing_Evidence/Bug_list.md) | Table of the issues found and resolved during development and testing, including some high level analysis. |

Each validation document contains the detailed evidence referenced in the README’s “Code Validation” section, ensuring full traceability between the summary and the underlying test artefacts.

Known issues are documented in the [README](/README.md)

---
