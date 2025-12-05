## ResourceToDbMain


The *ResourceToDbMapper* defines how a *Resource* is linked to physical database elements and how query behavior should be executed.

**Mapping & validation**

- Ensures that all resource attributes are mapped to valid database fields or derived expressions.  
- Verifies that join relationships are correctly defined.  

**Database structure**

- Specifies the primary table via `masterTable`.  
- Supports optional `additionalTables` for joined queries.  

**Query behavior**

- Configures filtering conditions, grouping, sorting, and pagination.  
- Supports data transformations, including aggregation functions, logical or numerical expressions, and regular expressions.  
  

By enforcing these rules, the ResourceToDbMapper guarantees that the
resource-to-database model is both valid and executable within the API.

                          
---
**Attributes:**

| Name | Type | Status | Description | Examples |
|:-----|:-----|:-------|:------------|:------------|
| `resource_name` | str | Optional | The name of the resource. Needs to be associated with an existing resource | era, fill 
| `masterTable` | str | Optional | The name of the database's master table |  
| `dbSchema` | str | Optional | The schema of the database's master table |  
| `primaryKey` | str | Optional | The primary key the database's master table |  
| `fields` | List[[TableAttribute](#tableattribute)] | Required | List of the mapping between the attributes of the resource and the fields in the database |  
| `additionalTables` | List[[AdditionalTable](#additionaltable)] | Required | Provides all the information about relations between the master table and other tables |  
| `groupBy` | List[str] | Optional | Applies grouping to the db resultset |  
| `defaultSort` | [SortedQuery](#sortedquery) | Required | Specifies the default sorting to the db resultset |  
| `pagination` | Literal[enabled, disabled] | Required | Paginate the db resultset |  
| `rowCounting` | Literal[enabled, disabled] | Required | Counting of the rows from the db resultset |



### Validators


**`validate_resource_model:`**
Perform cross-object validation between a Resource and its ResourceToDbMapper.

This validator runs **after** individual field validation and case normalization.
It enforces consistency between the resource specification (from YAML) and the
database mapping definition. Specifically, it checks:

1. Resource name consistency:
   - `resourceToDbMapper.resource_name` must equal `resource.resource_name`.

2. Mapping completeness:
   - At least one of `resourceToDbMapper.fields` or
     `resourceToDbMapper.additionalTables.fields` must be non-empty.
   - Every `resource.fields` attribute must be mapped to some DB attribute
     (direct field, expression, function, or case expression).

3. Attribute name correctness:
   - Every `attNameResource` in the mapper must correspond to an attribute
     defined in the Resource specification.
   - Each mapped field must define at least one of:
     `attNamedb`, `function`, `expression`, or `case_expression`.

4. GroupBy validation:
   - If a `groupBy` clause is provided, every DB attribute (`attNamedb`)
     without an aggregation function must appear in the `groupBy` list.

5. DefaultSort validation:
   - If a `defaultSort` is defined, each item must correspond to a valid
     `attNameResource`.

Errors are aggregated and raised as a single ValueError, making it easier
to spot multiple misconfigurations in one pass.


{% include-markdown "TableAttribute.md" %}

{% include-markdown "AdditionalTable.md" %}

{% include-markdown "RelationKey.md" %}

{% include-markdown "Condition.md" %}

{% include-markdown "Function.md" %}

{% include-markdown "Expression.md" %}

{% include-markdown "CaseExpression.md" %}

{% include-markdown "Regex.md" %}

{% include-markdown "DBColumnReference.md" %}

{% include-markdown "SortedQuery.md" %}

{% include-markdown "SortingSubSelect.md" %}

{% include-markdown "enum.md" %}