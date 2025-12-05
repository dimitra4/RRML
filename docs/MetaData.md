## MetaData


The *MetaData* provides descriptive and behavioral information for a resource attribute.
It can provide a human-readable title and description, indicate whether the attribute supports filtering
and sorting in queries, and specify any associated measurement units.

Together, these metadata properties enhance both API usability and
query capabilities without altering the structural definition of the attribute itself.

                          
---
**Attributes:**

| Name | Type | Status | Description | Examples |
|:-----|:-----|:-------|:------------|:------------|
| `title` | str | Optional |  |  
| `description` | str | Optional |  |  
| `searchable` | bool | Required | Indicates whether this attribute can be used in query filters |  
| `sortable` | bool | Required | Indicates whether this attribute can be used to order query results |  
| `units` | [Annotated](#annotated) | Optional | Unit of the attribute, as defined in the [*supported_units*](#SupportedTypesandUnits) YAML file |