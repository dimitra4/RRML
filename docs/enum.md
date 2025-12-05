## Constant Variables

---

### ArithmeticOperator

`StrEnum`  representing the basic arithmetic operators.
Each enum value has both a **short name** (used in YAML / DSL) and a corresponding **symbolic representation** (via the `symbol` property).

| Name   | Symbol | Description        |
|------------|--------|--------------------|
| `multiply` | `*`    | Represents multiply|
| `divide`   | `/`    | Represents divide  |
| `subtract` | `-`    | Represents subtract|
| `add`      | `+`    | Represents add     |

The name of the operator follows strict naming conventions. Referencing a non-existent name will raise an error.
Check [Error messages](errors.md)

??? Warning "Constant variables"

    Enums are contstant variables, the names of the enums follows strict naming conventions. Referencing a non-existent name will raise an error. [Error messages](errors.md)

```python title="add_number.py" linenums="1"
# Function to add two numbers
def add_two_numbers(num1, num2):
    return num1 + num2

# Example usage
result = add_two_numbers(5, 3)
print('The sum is:', result)
```

---

### ComparisonOperator

`StrEnum` representing the supported comparison operators used in filtering conditions (e.g. when building queries).  
Each enum value has both a **short name** (used in YAML / DSL) and a corresponding **symbolic representation** (via the `symbol` property).


| Name  | Symbol | Description |
|----------------|-------------------|-------------|
| `"eq"`         | `=`               | Equality check |
| `"ne"`         | `!=`              | Inequality check |
| `"lt"`         | `<`               | Strictly less than |
| `"lte"`        | `<=`              | Less than or equal |
| `"gt"`         | `>`               | Strictly greater than |
| `"gte"`        | `>=`              | Greater than or equal |
| `"like"`       | `like`            | Pattern matching (SQL `LIKE`) |
| `"in"`         | `in`              | Membership in a collection |
| `"is"`         | `is`              | Identity / null check |
| `"isnot"`      | `is not`          | Negated identity / null check |


```python linenums="1"
# Example usage
op = ComparisonOperator.EQUAL
print(op.value)   # "eq"
print(op.symbol)  # "="
```