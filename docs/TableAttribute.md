## TableAttribute



**Attributes:**

| Name | Type | Status | Description | Constraints |
|:-----|:-----|:-------|:------------|:------------|
| `attNamedb` | str | Optional | Same name as the name of the database attribute of the table |  |
| `attNameResource` | str | Optional | Same name as the name of the attribute of the resource |  |
| `function` | [Function](#function) | Required | Resource attribute is an aggregation, built-in or custom function |  |
| `expression` | [Expression](#expression) | Required | Resource attribute is an expression-combination of  db attributes, functions, views or values |  |
| `case_expression` | List[[CaseExpression](#caseexpression)] | Required | Resource attribute is a case expression. List of CASE branches: each with a `when` or `else` and a `then` clause |  |
| `sort` | [SortingSubSelect](#sortingsubselect) | Required | Sorting the subselect |  |



                          



                          
{% include-markdown "Function.md" %} 



                          
{% include-markdown "Expression.md" %} 



                          
{% include-markdown "CaseExpression.md" %} 



                          
{% include-markdown "SortingSubSelect.md" %}