from typing import (
    Literal,
    Optional,
    List,
    Any,
    Union
)
from pydantic import (
    BaseModel,
    Field,
    model_validator
)
from .resourceObjModel import Resource
from .enum import (
    ArithmeticOperator,
    ComparisonOperator
    )

class SortedQuery(BaseModel):
    fields: List[str] = Field(
        description="List of the accepted attributes to be sorted",
        min_items=1
    )
    order: Optional[Literal["asc", "desc"]] = Field(
        description="Accepted order for the sorted query",
        default=None
    )
    nulls: Optional[Literal["last", "first"]] = Field(
        description="Show nulls last or first",
        default=None
    )

class DBColumnReference(BaseModel):
    table: str = Field(
        description="The table name of the referenced column"
    )
    column: str = Field(
        description="The name of the column being referenced."
    )

class Condition(BaseModel):
    table: Optional[str] = Field(
        description="The table name of the referenced column",
        default=None
    )
    column: str = Field(
        description="The name of the database column that the condition applies to",
        examples=["run_number", "name", "status"]
    )
    operator: Union[ArithmeticOperator, ComparisonOperator] = Field(
        description=("The comparison or arithmetic operator to use in the condition"),
        examples=["eq"]
    )
    value: Union[str, int, float, bool, List[Union[str, int, float, bool]]] = Field(
        description=(
            "The value to compare the column against. It can be a string, number, boolean, or a list "
            "of such values (used with the `in` operator)."
        ),
        examples=["string_value", 42, True, [1, 2, 3]]
    )

# todo the operator check ** done
class CaseExpression(BaseModel):
    when: Condition = Field(
        description=(
            "A condition that must be met for this branch to apply. "
            "Must contain `column`, `operator`, and/or `value` and 'table name'. `value` is optional when the operator has the value `is` or `isnot` null"
        ),
        examples=[{"column": "stablebeam", "operator": "eq", "value": 1}]
    )
    else_: Optional[Union[str, int, float, bool, DBColumnReference, None]] = Field(
        default=None,
        alias="else",
        description="Fallback value if no conditions match"
    )
    then: Union[str, int, float, bool, DBColumnReference, None] = Field(
        description="The resulting value if this condition matches"
    )

# todo check if the column name hase the same name as one of the tableKey, targetKey
class Regex(BaseModel):
    column: str = Field(
        description="The name of the column to which the regular expression will be applied. It must match one of the defined relation keys",
        example="string_value: in the REGEXP_SUBSTR(string_value, '[^/]+', 1, 2) regex"
    )
    pattern: str = Field(
        description="The regular expression pattern",
        example="'[^/]+': in the REGEXP_SUBSTR(string_value, '[^/]+', 1, 2) regex"
    )
    groups: List[int] = Field(
        description="The grouping where the pattern will be applied",
        example="[1, 2]]: in the REGEXP_SUBSTR(string_value, '[^/]+', 1, 2) regex"
    ) 

class RelationKey(BaseModel):
    tableKey: str = Field (
        description="The name of the database column used to establish the relationship between the two tables. " \
        "If the column names differ, the `targetKey` segment must be specified"
    )
    targetKey: Optional[str] = Field (
        description="The name of the database column of the related table. " \
        "This segment is used when the column names differ",
        default=None
    )
    regex: Optional[Regex] = Field (
        description="A regular expression is applied to one of the relation keys",
        exaple="REGEXP_SUBSTR(string_value, '[^/]+', 1, 2)",
        default=None
    )

class Function(BaseModel):
    name: str = Field(
        description="Fully qualified name of the db function to call or any other built-in sql function",
        examples=["min", "max", "count", "avg", "sum", "round", "upper", "trim"]
        )
    params: Optional[List[Union["Expression", "FunctionCall", DBColumnReference, str, int, float, bool]]] = Field(
        default=None,
        description="Optional parameters to pass to the function"
    )
    distinct: Optional[bool] = Field(
        description="Distinct inside the function",
        examples="COUNT(DISTINCT value)",
        default=None 
    )

class FunctionCall(BaseModel):
    function: Function

class Expression(BaseModel):
    operator: ArithmeticOperator = Field(description="The arithmetic operator")
    left: Union[int, float, DBColumnReference, FunctionCall, "Expression"] = Field(
        description="The left-hand side of the expression"
    )
    right: Union[int, float, DBColumnReference, FunctionCall, "Expression"] = Field(
        description="The right-hand side of the expression"
    )

# todo if one of the attNamedb, expression, case_expression, function does not exists then raise an error ** done
class TableAttribute(BaseModel):
    attNamedb: Optional[str] = Field(
        description="Same name as the name of the database attribute of the table",
        default=None
    )
    attNameResource: str = Field(
        description="Same name as the name of the attribute of the resource"
    )
    function: Optional[Function] = Field(
        description="Resource attribute is an aggregation, built-in or custom function",
        default=None
    )
    expression: Optional[Expression] = Field(
        description="Resource attribute is an expression-combination of  db attributes, functions, views or values",
        default=None
    ) 
    case_expression: Optional[List[CaseExpression]] = Field(
        description="Resource attribute is a case expression. List of CASE branches: each with a `when` or `else` and a `then` clause",
        min_items=1,
        default=None
    )

class AdditionalTable(BaseModel):
    namedb: str = Field(
        description="The name of the database's additional table"
    )
    dbSchema: str = Field(
        description="The schema of the database's addtional table"
    )
    # todo to have specific naming for the relations ** done
    relation: Literal["innerJoin", "leftJoin", "asSubselect"] = Field(
        description=(
            "The relation between the master table and the additional table. "
            "Options:\n"
            "- `innerJoin`: Only include matching records from both tables\n"
            "- `leftJoin`: Include all records from master, and matched from related\n"
            "- `asSubselect`: Join via a subquery instead of directly"
        )
    )
    relationTable: str = Field(
        description="The name of the table to which the additional table is related. " \
        "This must match either a previously defined `namedb` in `additionalTables` or the `masterTable`"
    )
    relationKeys: List[RelationKey] = Field(
        description="The names of the relation keys (columns) of the tables related" 
    )
    conditions: Optional[List[Union[Condition, Regex]]] = Field(
        description="A list of conditions to apply as filters",
        default=None
    )
    fields: Optional[List[TableAttribute]] = Field(
        description="List of the mapping between the attributes of the resource and the fields in the database",
        default=None
    )

class ResourceToDbMapper(BaseModel):
    resource_name: str = Field(
        description="The name of the resource. Needs to be associated with an existing resource",
        pattern=r'^[a-zA-Z0-9_]+$',
        examples=["era", "fill"]
    )
    masterTable: str = Field(
        description="The name of the database's master table"
    )
    dbSchema: str = Field(
        description="The schema of the database's master table"
    )
    primaryKey: Optional[str] = Field(
        description="The primary key the database's master table",
        default=None
    )
    fields: Optional[List[TableAttribute]] = Field(
        description="List of the mapping between the attributes of the resource and the fields in the database",
        default=None
    )
    additionalTables: Optional[List[AdditionalTable]] = Field(
        description="Provides all the information about relations between the master table and other tables",
        default=None
    )
    # todo if grouping is there to test that the columns not referenced in the group by are in aggregated functions ** done
    groupBy: Optional[List[str]] = Field(
        description="Applies grouping to the db resultset",
        default=None
    )
    defaultSort: Optional[SortedQuery] = Field(
        description="Specifies the default sorting to the db resultset",
        default=None
    )
    pagination: Literal["enabled", "disabled"] = Field(
        description="Paginate the db resultset"
    )
    rowCounting: Literal["enabled", "disabled"] = Field(
        description="Counting of the rows from the db resultset"
    )

class ResourceToDbMappingSpec(BaseModel):
    resourceToDbMapper: ResourceToDbMapper = Field(
        description="Mapping of a resource to its database schema",
        validation_alias='resourceToDbMapper'
    )
    resource: Resource = Field(
        description="The specification of the resource."
    )

    @model_validator(mode="before")
    @classmethod
    def validate_fields(cls, v: dict[str, Any]) -> dict[str, Any]:
        errors = []
        if v is None:
            raise ValueError("Input data cannot be None")
        mapper = v.get("resourceToDbMapper")
        resource = v.get("resource")
        map_resource_name = mapper.get("resource_name")
        res_resource_name = resource.get("resource_name")

        if map_resource_name != res_resource_name:
            errors.append(
                f"Mismatch in resource names: resourceToDbMapper.resource_name (`{map_resource_name}`) "
                f"does not match resource.resource_name (`{res_resource_name}`)"
            )
        
        fields = mapper.get("fields", []) or []
        additionalTable = mapper.get("additionalTables", []) or []
        # Collect fields from additionalTables
        for table in additionalTable:
            add_table_fields = table.get("fields", []) or []
        # add the two lists in another list, otherwise it affects the final `fields`` value in the pydantic model
        allFields = fields + add_table_fields or []

        if not allFields:
            errors.append(
                f"Both resourceToDbMapper.fields and resourceToDbMapper.additionalTables.fields cannot be empty at the same time."
                f"If both are empty, no select list attributes will be included in the final query"
            )

        groupBy = mapper.get("groupBy", [])
        defaultSort = mapper.get("defaultSort")

        # Collect all allowed attNamedb from primary fields
        allowed_fields_attNamedb = {}
        # Collect all allowed attNameResource from primary fields
        allowed_fields_attNameResource= []

        for field in allFields:
            attResource = field.get("attNameResource")
            allowed_fields_attNameResource.append(attResource)

            att = field.get("attNamedb")
            case_expression = field.get("case_expression")
            expression = field.get("expression")
            function = field.get("function")
            if att:
                allowed_fields_attNamedb[att] = field.get("function")  # function may be None
            if not att and not case_expression and not expression and not function:
                errors.append(
                    f"fields.attNamedb, fields.function, fields.expression, fields.case_expression  cannot be empty at the same time.\n"
                    f"If all are empty, no db attribute, function, expression is being assigned to the resource attribute fields.attNameResource field: `{attResource}`\n"
                    f"If a function needs to appear within an expression—or vice versa—they must be nested in a tree-like structure"
                )
                
        # Validation for groubBy list. If an item does not exist in select list as attribute(`attNamedb`) or aggregated function, then raise error. 
        # The items of the list need to have the same naming as the `attNamedb`
        if groupBy:
            for att_name, func in allowed_fields_attNamedb.items():
                if att_name not in groupBy and func is None:
                    errors.append(
                        f"Invalid reference of attribute: '{att_name}' in fields\n"
                        f"→ It must be defined either in the `groub by` segment or used within an aggregation function.")
        
        # Validation for defaultSort list. If an item does not exist in select list as attribute(`attNameResource`), then raise error. 
        # The items of the list need to have the same naming as the `attNameResource`
        if defaultSort:
            for att_name in defaultSort.get("fields"):
                if att_name not in allowed_fields_attNameResource:
                    errors.append(
                        f"Invalid reference of attribute: '{att_name}' in defaultSort.fields\n"
                        f"→ There is no attribute with this name in the `attNameResource` fields.")
                        
        if errors:
            raise ValueError(f"{len(errors)} errors raised:\n - " + "\n - ".join(errors))

        return v