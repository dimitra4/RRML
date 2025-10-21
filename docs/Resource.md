## Resource



**Attributes:**

| Name | Type | Status | Description | Constraints |
|:-----|:-----|:-------|:------------|:------------|
| `resource_name` | str | Optional | The name of the resource. All classes will be named using this name | Examples: era, fill, resource_1, data2024 |
| `version` | str | Optional | Release of a project, marked by a version number  | Examples: 1.0.0 |
| `hasMeta` | bool | Optional |  |  |
| `fields` | List[[Attribute](#attribute)] | Required | List of the attributes of the resource |  |



                          




                          
{% include-markdown "Attribute.md" %}