## Condition



**Attributes:**

| Name | Type | Status | Description | Constraints |
|:-----|:-----|:-------|:------------|:------------|
| `table` | str | Optional | The table name of the referenced column |  |
| `column` | str | Optional | The name of the database column that the condition applies to | Examples: run_number, name, status |
| `operator` | [ArithmeticOperator](ArithmeticOperator.md), [ComparisonOperator](ComparisonOperator.md) | Required | The comparison or arithmetic operator to use in the condition | Examples: eq |
| `value` | str, int, float, bool, List[str, int, float, bool] | Optional | The value to compare the column against. It can be a string, number, boolean, or a list of such values (used with the `in` operator). | Examples: string_value, 42, True, [1, 2, 3] |