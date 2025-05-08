## Expression



**Attributes:**

| Name | Type | Status | Description | Constraints |
|:-----|:-----|:-------|:------------|:------------|
| `operator` | [ArithmeticOperator](ArithmeticOperator.md) | Required | The arithmetic operator |  |
| `left` | int, float, [DBColumnReference](DBColumnReference.md), [FunctionCall](FunctionCall.md), [Expression](Expression.md) | Required | The left-hand side of the expression |  |
| `right` | int, float, [DBColumnReference](DBColumnReference.md), [FunctionCall](FunctionCall.md), [Expression](Expression.md) | Required | The right-hand side of the expression |  |