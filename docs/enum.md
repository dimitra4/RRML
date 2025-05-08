# Constant Variables (Enums) 

[tutorial mkdocs-material](https://jameswillett.dev/getting-started-with-material-for-mkdocs/#collapsible-admonitions)

### `ArithmeticOperator`
Enum representing the basic arithmetic operators.

| Operator   | Symbol | Description        |
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











