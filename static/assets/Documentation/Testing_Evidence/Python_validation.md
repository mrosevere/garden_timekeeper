# Python Validation

All Python has been validated against the [Pep8 standards](https://pep8ci.herokuapp.com/)

The process was :
1. Copy the source code and paste it into the [Pep8 validator](https://pep8ci.herokuapp.com/)
2. Record the results below. Any issues are logged in the [GitHub Project](https://github.com/users/mrosevere/projects/17) as bugs.

In addition, Flake8 was installed into Visual Studio Code IDE for instant feedback.

## Results

### Accounts App

| Python File | Result | Issues found & resolved |
| ----------- | ----------- | ----------- |
| accounts\forms.py | All clear, no errors found | |
| accounts\models.py | All clear, no errors found | |
| accounts\urls.py | All clear, no errors found | |
| accounts\views.py | All clear, no errors found | |

### Core App

| Python File | Result | Issues found & resolved |
| ----------- | ----------- | ----------- |
| core\month_filters.py | All clear, no errors found | |
| core\navigation_tags.py | All clear, no errors found | |
| core\forms.py | All clear, no errors found | |
| core\models.py | All clear, no errors found | |
| core\urls.py | All clear, no errors found | |
| core\views.py | xxxx | [issue-259](https://github.com/mrosevere/garden_timekeeper/issues/259) |



### Django App

| Python File | Result | Issues found & resolved |
| ----------- | ----------- | ----------- |
| garden_timekeeper\settings.py | All clear, no errors found | |
| garden_timekeeper\urls.py | All clear, no errors found | |


### Unit Tests

| Python File | Result | Issues found & resolved |
| ----------- | ----------- | ----------- |
| accounts\test_auth_views.py | All clear, no errors found | |
| core\test_bed_views.py | All clear, no errors found | |
| core\test_beds.py | All clear, no errors found | |
| core\test_calendar_views.py | All clear, no errors found | |
| core\test_models.py | All clear, no errors found | |
| core\test_plant_views.py | All clear, no errors found | |
| core\test_task_views.py | All clear, no errors found | [issue-260](https://github.com/mrosevere/garden_timekeeper/issues/260)|
| core\test_template_tags.py | All clear, no errors found | |
