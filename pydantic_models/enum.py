from enum import StrEnum

# Define the Enum for valid attribute data types
class FieldType(StrEnum):
    datetime_iso = "datetime"
    string = "string"
    text = "longstring"
    integer32 = "smallinteger"
    integer64 = "integer"
    biginteger = "biginteger"
    timeinterval_int = "timeinterval_int"
    timeinterval_double = "timeinterval_double"
    float = "float"
    double = "double"
    boolean = "boolean"
    binarystring = "binarystring"
    decimal = "decimal"

class ArithmeticOperator(StrEnum):
    MULTIPLY = "multiply"
    DIVIDE = "divide"
    SUBTRACT = "subtract"
    ADD = "add"

    @property
    def symbol(self) -> str:
        return {
            ArithmeticOperator.MULTIPLY: "*",
            ArithmeticOperator.DIVIDE: "/",
            ArithmeticOperator.SUBTRACT: "-",
            ArithmeticOperator.ADD: "+",
        }[self]

class ComparisonOperator(StrEnum):
    EQUAL = "eq"
    NOEQUAL = "ne"
    LESS_THAN = "lt"
    LESS_THAN_EQUAL = "lte"
    GREATER_THAN = "gt"
    GREAT_THAN_EQUAL = "gte"
    LIKE = "like"
    IN = "in"
    IS = "is"
    ISNOT = "isnot"

    @property
    def symbol(self) -> str:
        return {
            ComparisonOperator.EQUAL: "=",
            ComparisonOperator.NOEQUAL: "!=",
            ComparisonOperator.LESS_THAN: "<",
            ComparisonOperator.LESS_THAN_EQUAL: "<=",
            ComparisonOperator.GREATER_THAN: ">",
            ComparisonOperator.GREAT_THAN_EQUAL: ">=",
            ComparisonOperator.LIKE: "like",
            ComparisonOperator.IN: "in",
            ComparisonOperator.IS: "is",
            ComparisonOperator.ISNOT: "is not",
        }[self]