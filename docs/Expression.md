## Expression



**Attributes:**

| Name | Type | Status | Description | Constraints |
|:-----|:-----|:-------|:------------|:------------|
| `operator` | [ArithmeticOperator](#arithmeticoperator) | Required | The arithmetic operator |  |
| `left` | int, float, [DBColumnReference](#dbcolumnreference), [FunctionCall](#functioncall), [Expression](#expression) | Required | The left-hand side of the expression |  |
| `right` | int, float, [DBColumnReference](#dbcolumnreference), [FunctionCall](#functioncall), [Expression](#expression) | Required | The right-hand side of the expression |  |



                          

    
{% include-markdown "enum.md" %} 



                          
{% include-markdown "DBColumnReference.md" %} 



                          
{% include-markdown "DBColumnReference.md" %}