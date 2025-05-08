## TableAttribute



**Attributes:**

| Name | Type | Status | Description | Constraints |
|:-----|:-----|:-------|:------------|:------------|
| `attNamedb` | str | Optional | Same name as the name of the database attribute of the table |  |
| `attNameResource` | str | Optional | Same name as the name of the attribute of the resource |  |
| `function` | [Function](Function.md) | Required | Resource attribute is an aggregation, built-in or custom function |  |
| `expression` | [Expression](Expression.md) | Required | Resource attribute is an expression-combination of  db attributes, functions, views or values |  |
| `case_expression` | List[[CaseExpression](CaseExpression.md)] | Required | Resource attribute is a case expression. List of CASE branches: each with a `when` or `else` and a `then` clause |  |