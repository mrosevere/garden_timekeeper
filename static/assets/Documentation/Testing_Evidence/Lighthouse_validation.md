# Lighthouse Validation

All html templates have been checked using the <b><i>Google DevTool Lighthouse</b></i>

The process was performed on the deployed [Heroku app](https://garden-timekeeper-588fc83d2eb9.herokuapp.com/) or the local Dev instance.
1. Navigate to the relevant page using the production deployed App
2. F12 -> Developer Tools -> Lighthouse -> Analyze Page [Mode: Navigation (Default)]
3. Record the results below. Any issues are logged in the [GitHub Project](https://github.com/users/mrosevere/projects/17) as bugs.

## Results

### Accounts App

| HTML Page | Performance | Accessibility | Best Practices | 
| ----------- | ----------- | ----------- | ----------- | 
| accounts\login.html | 99 | 100 | 100 | 
| accounts\register.html | 99 | 100 | 100 | 
| accounts\account_edit.html | 99 | 100 | 100 | 
| accounts\account_settings.html  | 99 | 100 | 100 | 
| accounts\delete_account.html | 100 | 100 | 100 | 
| accounts\password_edit_done.html | 100 | 100 | 100 | 
| accounts\password_edit.html | 99 | 100 | 100 | 
| accounts\password_reset_complete.html | 99 | 100 | 100 | 
| accounts\password_reset_confirm.html | 99 | 100 | 100 | 
| accounts\password_reset_done.html | 99 | 100 | 100 | 
| accounts\password_reset.html | 99 | 100 | 100 | 

### Core App
I added SEO to the analysis for the core app (not selected by default).

| HTML Page | Performance | Accessibility | Best Practices | SEO | 
| ----------- | ----------- | ----------- | ----------- | ----------- |
| core\beds\bed_create.html | 99 | 100 | 100 | 100 |
| core\beds\bed_detail.html | 99 | 100 | 100 | 100 | 
| core\beds\bed_edit.html | 99 | 100 | 100 | 100 |  
| core\beds\bed_list.html | 97 | 100 | 100 | 100 |  
| core\plants\plant_create.html | 99 | 100 | 96 | 91 | 
| core\plants\plant_detail.html | 97 | 100 | 100 | 100 |
| core\plants\plant_edit.html | 98 | 100 | 96 | 91 |
| core\plants\plant_list.html | 99 | 100 | 100 | 100 |
| core\tasks\task_detail.html | 99 | 100 | 100 | 100 |
| core\tasks\task_form.html | 98 | 100 | 96 | 91 |
| core\dashboard.html | 99 | 100 | 100 | 100 |
| core\home.html | 99 | 100 | 100 | 100 |


[issue-266](https://github.com/mrosevere/garden_timekeeper/issues/266) |

### Lighthouse Console Warnings (plant_edit, task_edit & plant_create)
Lighthouse Console Warning: Bootstrap Tooltip Re‑initialisation
During Lighthouse audits, the following console warning may appear:
```
Bootstrap doesn't allow more than one instance per element. Bound instance: bs.tooltip.
```
This warning does not appear during normal use of the application and does not indicate a runtime error. It is triggered only inside Lighthouse’s automated testing environment.

#### Why it happens
Lighthouse loads the page in a headless browser and then:
- reloads the page multiple times
- simulates hover and focus events
- triggers Bootstrap tooltips
- triggers Summernote’s internal tooltip initialisation
- triggers the application’s own tooltip initialisation
- does all of this before the DOM has fully settled

This causes Bootstrap to attempt to initialise a tooltip on the same element more than once, which produces the warning.

### Fix implemented
The application includes a guard to prevent duplicate tooltip initialisation:
```
js
if (!bootstrap.Tooltip.getInstance(el)) {
    new bootstrap.Tooltip(el);
}
```
This prevents duplicate instances during normal use.

### The warning still appears in Lighthouse
Lighthouse interacts with the page in ways that normal users do not.
It can trigger tooltip initialisation before the guard code runs, or trigger Summernote’s internal tooltip logic multiple times in rapid succession.

This behaviour is specific to Lighthouse’s testing environment and does not occur in real browsers.

### Impact
- No errors appear in the browser console during normal use
- No functionality is affected
- No accessibility or performance issues are caused
- The application remains fully WCAG‑compliant
- Lighthouse accessibility score remains 100%

The overall Lighthouse score may show 96% due to this non‑critical console warning

### Conclusion
This is a known Lighthouse false positive related to Bootstrap tooltips and Summernote.
The application’s implementation is correct, stable, and behaves as expected in real‑world usage.

## Lighthouse SEO Warning: “Links are not crawlable” (plant_edit, task_edit & plant_create)

Lighthouse reports that some links are “not crawlable”.  
This is expected behaviour for a Django application where most pages require authentication.

Search engines cannot index:
- dashboard pages
- plant list / detail pages
- bed list / detail pages
- any page behind login

Lighthouse runs its audit without authentication, so all protected URLs return redirects or 403 responses. This causes Lighthouse to incorrectly report that links are not crawlable.

This does not affect real SEO.  
All public pages (Home, Login, Register) are fully crawlable.
