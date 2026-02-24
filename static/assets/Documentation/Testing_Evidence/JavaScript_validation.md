# JavaScript validation

All JavaScript files have been checked using [jshint](https://jshint.com/)

The process was :
1. Copy the source code and paste it into the [jshint](https://jshint.com/)
2. Record the results below. Any issues are logged in the [GitHub Project](https://github.com/users/mrosevere/projects/17) as bugs.

## Results


| JS file | Result | Issues found & resolved |
| ----------- | ----------- | ----------- |
| \static\assets\js\core\dom.js | There are 3 functions in this file. <br>Function with the largest signature take 2 arguments, while the median is 2.<br>Largest function has 2 statements in it, while the median is 1.<br>The most complex function has a cyclomatic complexity value of 2 while the median is 1. | All warnings resolved |
| \static\assets\js\core\filters.js | Metrics<br>There are 2 functions in this file.<br>Function with the largest signature take 2 arguments, while the median is 1.5.<br>Largest function has 4 statements in it, while the median is 2.5.<br>The most complex function has a cyclomatic complexity value of 6 while the median is 3.5. | All warnings resolved |
| \static\assets\js\core\pagination.js | Metrics<br>There are 7 functions in this file.<br>Function with the largest signature take 2 arguments, while the median is 0.<br>Largest function has 3 statements in it, while the median is 1.<br>The most complex function has a cyclomatic complexity value of 1 while the median is 1. | All warnings resolved |
| \static\assets\js\core\utils.js | Metrics<br>There are 4 functions in this file.<br>Function with the largest signature take 2 arguments, while the median is 1.<br>Largest function has 2 statements in it, while the median is 1.5.<br>The most complex function has a cyclomatic complexity value of 2 while the median is 1. | All warnings resolved |
| \static\assets\js\dashboard.js | Metrics<br>There are 20 functions in this file.<br>Function with the largest signature take 3 arguments, while the median is 0.<br>Largest function has 23 statements in it, while the median is 3.<br>The most complex function has a cyclomatic complexity value of 10 while the median is 2. | All warnings resolved |
| \static\assets\js\plant_detail.js | Metrics<br>There are 15 functions in this file.<br>Function with the largest signature take 2 arguments, while the median is 0.<br>Largest function has 23 statements in it, while the median is 3.<br>The most complex function has a cyclomatic complexity value of 8 while the median is 2. | All warnings resolved |
| \static\assets\js\script.js | Metrics<br>There are 12 functions in this file.<br>Function with the largest signature take 2 arguments, while the median is 0.<br>Largest function has 10 statements in it, while the median is 4.5.<br>The most complex function has a cyclomatic complexity value of 6 while the median is 2. | Two warnings<br>212	Do not use 'new' for side effects.<br>219	Do not use 'new' for side effects. |

### Known Issue

The only remaining Warning is on \static\assets\js\script.js :
```
Two warnings
212	Do not use 'new' for side effects.
219	Do not use 'new' for side effects.
```

JSHint.com has a known bug with W064
This is a long‑standing issue:
JSHint.com cannot reliably suppress W064 (“Do not use 'new' for side effects”) when the new appears inside a callback.
This is because the online version uses an older parser that mishandles:
- ES6 classes
- Bootstrap’s constructor pattern
- jQuery .each() callbacks
- inline suppression comments