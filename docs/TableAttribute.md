## TableAttribute


Maps a **resource attribute** to its corresponding **database attribute** 
or derived expression.

A `TableAttribute` can represent:

- a direct database column mapping,
- an aggregation or built-in SQL function,
- a custom arithmetic expression,
- or a CASE expression with conditional branches.

**Examples YAML**

```yaml
- attNamedb: "fill_number"
  attNameResource: "fill_number"
```
corresponds to:
```sql
SELECT fill_number as fill_number
```

                          
---
**Attributes:**

| Name | Type | Status | Description | Examples |
|:-----|:-----|:-------|:------------|:------------|
| `attNamedb` | str | Optional | The name of the database column (attribute of the table) |  
| `attNameResource` | str | Required | The name of the attribute as it appears in the resource model |  
| `function` | [Function](#function) | Optional | Resource attribute is computed using an aggregation, built-in, or custom function |  
| `expression` | [Expression](#expression) | Optional | Resource attribute is an expression-combination of  db attributes, functions, views or values |  
| `case_expression` | List[[CaseExpression](#caseexpression)] | Optional | Resource attribute is a case expression. List of CASE branches: each with a `when` or `else` and a `then` clause |  
| `sort` | [SortingSubSelect](#sortingsubselect) | Required | Sorting the subselect |