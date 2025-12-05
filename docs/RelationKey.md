## RelationKey


Represents the **key mapping** between two related tables.
 A `RelationKey` defines how the join between two tables is performed, by specifying which column(s) act as the keys. 
 Optionally, a regex transformation can be applied to one of the keys.

 If both tables share the same key name, only `tableKey` is required.  
 If the key names differ, then `targetKey` must also be provided to reference the column name in the related table.
 
                          
---
**Attributes:**

| Name | Type | Status | Description | Examples |
|:-----|:-----|:-------|:------------|:------------|
| `tableKey` | str | Required | The name of the database column used to establish the relationship between the two tables. If the column names differ, the `targetKey` segment must be specified |  
| `targetKey` | str | Optional | The name of the database column of the related table. This segment is used when the column names differ |  
| `regex` | [Regex](#regex) | Optional | A regular expression is applied to one of the relation keys |