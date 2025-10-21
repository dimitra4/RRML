## AdditionalTable



**Attributes:**

| Name | Type | Status | Description | Constraints |
|:-----|:-----|:-------|:------------|:------------|
| `namedb` | str | Optional | The name of the database's additional table |  |
| `dbSchema` | str | Optional | The schema of the database's addtional table |  |
| `relation` | Literal[innerJoin, leftJoin, asSubselect] | Required | The relation between the master table and the additional table. Options:
- `innerJoin`: Only include matching records from both tables
- `leftJoin`: Include all records from master, and matched from related
- `asSubselect`: Join via a subquery instead of directly |  |
| `relationTable` | str | Optional | The name of the table to which the additional table is related. This must match either a previously defined `namedb` in `additionalTables` or the `masterTable` |  |
| `relationKeys` | List[[RelationKey](#relationkey)] | Required | The names of the relation keys (columns) of the tables related |  |
| `conditions` | List[[Condition](#condition), [Regex](#regex)] | Required | A list of conditions to apply as filters |  |
| `fields` | List[[TableAttribute](#tableattribute)] | Required | List of the mapping between the attributes of the resource and the fields in the database |  |



                          





                          
{% include-markdown "RelationKey.md" %} 



                          
{% include-markdown "Condition.md" %} 



                          
{% include-markdown "TableAttribute.md" %}