## Attribute



**Attributes:**

| Name | Type | Status | Description | Constraints |
|:-----|:-----|:-------|:------------|:------------|
| `name` | str | Optional | Name of the attribute of the resource | Examples: id, start_time, run_number |
| `type` | str | Optional | The data type of the attribute of the resource according to the standardized mapping_types YAML file |  |
| `isKey` | bool | Optional | Explicitly determine true if the attribute is the actual identifier of the resource |  |
| `meta` | [MetaData](#metadata) | Required | The meta data of the attribute |  |



                          




                          
{% include-markdown "MetaData.md" %}