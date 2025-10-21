## RelationKey



**Attributes:**

| Name | Type | Status | Description | Constraints |
|:-----|:-----|:-------|:------------|:------------|
| `tableKey` | str | Optional | The name of the database column used to establish the relationship between the two tables. If the column names differ, the `targetKey` segment must be specified |  |
| `targetKey` | str | Optional | The name of the database column of the related table. This segment is used when the column names differ |  |
| `regex` | [Regex](#regex) | Required | A regular expression is applied to one of the relation keys |  |



                          



                          
{% include-markdown "Regex.md" %}