# HTML Validation

All html templates have been checked using the [W3 HTML Validator](https://validator.w3.org/)

The process was performed on the deployed [Heroku app](https://garden-timekeeper-588fc83d2eb9.herokuapp.com/)
1. Navigate to the relevant page using the production deployed App
2. Right-click -> View Source
3. Copy the source code and paste it into the [W3 Validator](https://validator.w3.org/#validate_by_input)
4. Record the results below. Any issues are logged in the [GitHub Project](https://github.com/users/mrosevere/projects/17) as bugs.

> **ℹ️ NOTE:**
> On HTML Validation: The application uses Summernote to allow rich‑text notes. Because Summernote allows users to insert headings, inline styles, and other HTML elements, user‑generated content may trigger HTML validation warnings (e.g., nested headings, deprecated <font> tags). These warnings originate from user input rather than template markup.


## Results

### Accounts App

| HTML Page | Result | Issues found & resolved |
| ----------- | ----------- | ----------- |
| accounts\login.html | Document checking completed. No errors or warnings to show. ||
| accounts\register.html | Document checking completed. No errors or warnings to show. ||
| accounts\account_edit.html | Document checking completed. No errors or warnings to show. ||
| accounts\account_settings.html | Document checking completed. No errors or warnings to show. ||
| accounts\delete_account.html | Document checking completed. No errors or warnings to show. ||
| accounts\password_edit_done.html | Document checking completed. No errors or warnings to show. ||
| accounts\password_edit.html | Document checking completed. No errors or warnings to show. ||
| accounts\password_reset_complete.html | Document checking completed. No errors or warnings to show. ||
| accounts\password_reset_confirm.html | Document checking completed. No errors or warnings to show. ||
| accounts\password_reset_done.html | Document checking completed. No errors or warnings to show. ||
| accounts\password_reset.html| Document checking completed. No errors or warnings to show. ||

### Core App

| HTML Page | Result |  Issues found & resolved |
| ----------- | ----------- | ----------- |
| core\beds\bed_create.html | 
| core\beds\bed_detail.html |  Document checking completed. No errors or warnings to show. | |
| core\beds\bed_edit.html |  Document checking completed. No errors or warnings to show. | |
| core\beds\bed_list.html | Document checking completed. No errors or warnings to show.| [issue-272](https://github.com/mrosevere/garden_timekeeper/issues/272)|
| core\plants\plant_create.html | Document checking completed. No errors or warnings to show. | |
| core\plants\plant_detail.html | Document checking completed. No errors or warnings to show. | |
| core\plants\plant_edit.html | Document checking completed. No errors or warnings to show. | |
| core\plants\plant_list.html | Document checking completed. No errors or warnings to show. | |
| core\tasks\task_detail.html | Document checking completed. No errors or warnings to show.| [issue-269](https://github.com/mrosevere/garden_timekeeper/issues/269)|
| core\tasks\task_form.html | Document checking completed. No errors or warnings to show.||
| core\base.html | Document checking completed. No errors or warnings to show. ||
| core\dashboard.html | Document checking completed. No errors or warnings to show. |[issue-269](https://github.com/mrosevere/garden_timekeeper/issues/269)|
| core\home.html | Document checking completed. No errors or warnings to show. ||
