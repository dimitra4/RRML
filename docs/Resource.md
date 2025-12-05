## Resource


The *Resource* model defines the representation of a domain entity exposed through the API.

- Each resource has a unique `resource_name` and may include a `version` for documentation and lifecycle tracking.
- A resource is composed of a list of `Attribute` elements. Each attribute carries:
    - **Structural metadata** (e.g. its name, description, units).
    - **Behavioral flags** that determine how it can be used in the API and in internal query logic (e.g. filtering, sorting, or key fields).

Together, these properties ensure that a Resource can be consistently documented, validated, and mapped to underlying database entities.

                          
---
**Attributes:**

| Name | Type | Status | Description | Examples |
|:-----|:-----|:-------|:------------|:------------|
| `resource_name` | str | Required | The name of the resource. All classes will be named using this name | era, fill, resource_1, data2024 
| `version` | str | Required | Release of a project, marked by a version number  | 1.0.0 
| `hasMeta` | bool | Optional |  |  
| `fields` | List[[Attribute](#attribute)] | Required | List of the attributes of the resource |  



### Validators


**`validate_resource_model:`**
Perform post-validation checks on a Resource definition. This validator runs **after** field-level validation and case normalization.
It ensures that every Resource has a proper identifier field defined.

Specifically, it enforces:

1. **Key field requirement**
    - At least one attribute in `resource.fields` must have `isKey=True`.
    - This key field serves as the unique identifier of the Resource.
    - Composite identifiers are also supported by marking multiple attributes with `isKey=True`.


If no key field is found, a ValueError is raised, clearly listing the issue.

This safeguard guarantees that every Resource defined in the specification
can be uniquely identified, which is a prerequisite for consistent mapping
to database entities and for stable API resource behavior.