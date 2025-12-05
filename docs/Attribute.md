## Attribute


The *Attribute* defines a single field of a Resource. Each attribute has
a name and type, may be marked as the key identifier of the resource, and
can optionally include additional metadata for documentation and query
behavior.

                          
---
**Attributes:**

| Name | Type | Status | Description | Examples |
|:-----|:-----|:-------|:------------|:------------|
| `name` | str | Required | Name of the attribute of the resource | id, start_time, run_number 
| `type` | str | Required | The data type of the attribute of the resource according to the standardized mapping_types YAML file |  
| `isKey` | bool | Optional | Explicitly determine true if the attribute is the actual identifier of the resource |  
| `meta` | [MetaData](#metadata) | Optional | The meta data of the attribute |