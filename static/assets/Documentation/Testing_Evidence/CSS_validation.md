# CSS Validation

## Process
1. Navigate to the deployed site.
2. Right Click -> View Source.
3. Click on the [css link](https://garden-timekeeper-588fc83d2eb9.herokuapp.com/static/assets/css/style.css)
4. Copy the CSS into [JIGSAW](https://jigsaw.w3.org/css-validator/)

## Results

<b> No errors found: </b>
```
    W3C CSS Validator results for https://garden-timekeeper-588fc83d2eb9.herokuapp.com/static/assets/css/style.css (CSS level 3 + SVG)
    Congratulations! No Error Found.
    This document validates as CSS level 3 + SVG !
```

<b> 3 warnings: </b>
<br>
```
    URI : https://garden-timekeeper-588fc83d2eb9.herokuapp.com/static/assets/css/style.css

    | Row | Warning |
    | ---- | ---- |
    | 79  |		::-webkit-credentials-auto-fill-button is a vendor extended pseudo-element |
    | 109 |	.btn-secondary	Same color for background-color and border-color |
    | 115 | .btn-secondary:hover	Same color for background-color and border-color |
```
These have been reviewed and deemed acceptable.