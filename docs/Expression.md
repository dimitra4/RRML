## Expression


Represents an arithmetic expression.

An `Expression` is a binary operation composed of:

- an [`ArithmeticOperator`](#arithmeticoperator)
- a `left` operand
- a `right` operand

Both operands may be literals, column references, nested function calls, or even nested expressions.

**Example YAML**

```yaml
expression:
    operator: "subtract"
    left: {table: "fills", column: "stop_time"}
    right: {table: "fills", column: "start_time"}
```

corresponds to:
```sql
(fills.stop_time - fills.start_time)
```

                          
---
**Attributes:**

| Name | Type | Status | Description | Examples |
|:-----|:-----|:-------|:------------|:------------|
| `operator` | [ArithmeticOperator](#arithmeticoperator) | Required | The arithmetic operator |  
| `left` | int, float, [DBColumnReference](#dbcolumnreference), [FunctionCall](#functioncall), [Expression](#expression) | Required | The left-hand side of the expression |  
| `right` | int, float, [DBColumnReference](#dbcolumnreference), [FunctionCall](#functioncall), [Expression](#expression) | Required | The right-hand side of the expression |