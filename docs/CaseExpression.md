## CaseExpression



**Attributes:**

| Name | Type | Status | Description | Constraints |
|:-----|:-----|:-------|:------------|:------------|
| `when` | [Condition](#condition) | Required | A condition that must be met for this branch to apply. Must contain `column`, `operator`, and/or `value` and 'table name'. `value` is optional when the operator has the value `is` or `isnot` null | Examples: {'column': 'stablebeam', 'operator': 'eq', 'value': 1} |
| `else_` | str | Optional | Fallback value if no conditions match |  |
| `then` | str | Optional | The resulting value if this condition matches |  |



                          

                          
{% include-markdown "Condition.md" %}