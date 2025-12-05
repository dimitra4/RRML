## Condition


Represents a **WHERE condition** applied in a query.
A `Condition` defines a table, column, operator, and comparison value. Operators may be arithmetic or comparison operators.  
Multiple conditions can also be combined in a list.

**Example YAML**

```yaml
conditions:
  - column: "stable_beams"  
    operator: "eq"
    value: 1                   
  - column: "enabled" 
    operator: "eq"
    value: 1      
```

                          
---
**Attributes:**

| Name | Type | Status | Description | Examples |
|:-----|:-----|:-------|:------------|:------------|
| `table` | str | Optional | The table name of the referenced column |  
| `column` | str | Required | The name of the database column that the condition applies to | run_number, name, status 
| `operator` | [ArithmeticOperator](#arithmeticoperator), [ComparisonOperator](#comparisonoperator) | Required | The comparison or arithmetic operator to use in the condition | eq 
| `value` | str, int, float, bool, List[str, int, float, bool] | Required | The value to compare the column against. It can be a string, number, boolean, or a list of such values (used with the `in` operator). | string_value, 42, True, [1, 2, 3]