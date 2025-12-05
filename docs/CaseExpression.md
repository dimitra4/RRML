## CaseExpression


Represents a **CASE expression** in SQL.
A `CaseExpression` evaluates a condition and returns a value via
the `then` clause. If no `when` branch matches, the optional `else`
provides a fallback value.

**Example YAML**

```yaml
case_expression: 
  - when: { column: "start_time", operator: "isnot", value: "null"}
    then: 1
```

corresponds to:
```sql
CASE
  WHEN start_time IS NOT NULL THEN 1
END
```

                          
---
**Attributes:**

| Name | Type | Status | Description | Examples |
|:-----|:-----|:-------|:------------|:------------|
| `when` | [Condition](#condition) | Required | A condition that must be met for this branch to apply. Must contain `column`, `operator`, and/or `value` | {'column': 'stablebeam', 'operator': 'eq', 'value': 1} 
| `else_` | str | Required | Fallback value if no conditions match |  
| `then` | str | Required | The resulting value if this condition matches |