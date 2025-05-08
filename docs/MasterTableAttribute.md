## MasterTableAttribute



### Fields

| Name | Type | Status | Description | Constraints |
|:-----|:-----|:-------|:------------|:------------|
| `attNamedb` | str | Optional | Same name as the name of the database attribute of the table |  |
| `attNameResource` | str | Optional | Same name as the name of the attribute of the resource |  |
| `expression` | [Expression](Expression.md) | Required | Database attribute is an expression-combination of  db attributes, functions, views or values |  |