## AdditionalTable


Represents an **additional table** that can be joined with the master table
or another additional table in order to enrich the resource definition.

Joins can be defined as `innerJoin`, `leftJoin`, `rightJoin`, or as a `subselect`.

**Example YAML**

```yaml
additionalTables:
  - namedb: "eras"
    dbSchema: "cms_oms"
    relation: "leftJoin"
    relationTable: *masterTable
    relationKeys:
      - tableKey: "era_id"          # Same name in both tables
        # - tablekey: "status"      # Different names
        #   targetKey: "era_status"
    fields: 
      - attNamedb: "name"
        attNameResource: "era""
```

corresponds to:
```sql
SELECT eras.name as era
FROM cms_oms.fills fills
LEFT JOIN cms_oms.eras eras
  ON fills.era_id = eras.era_id
```

                          
---
**Attributes:**

| Name | Type | Status | Description | Examples |
|:-----|:-----|:-------|:------------|:------------|
| `namedb` | str | Required | The name of the database's additional table |  
| `dbSchema` | str | Required | The schema of the database's addtional table |  
| `relation` | Literal[innerJoin, leftJoin, asSubselect, rightJoin] | Required | The relation between the master table and the additional table. Options:<br>- `innerJoin`: Only include matching records from both tables<br>- `leftJoin`: Include all records from master, and matched from related<br>- `rightJoin`: Include all records from related, and matched from master<br>- `asSubselect`: Join via a subquery instead of directly |  
| `relationTable` | str | Required | The name of the table to which the additional table is related. This must match either a previously defined `namedb` in `additionalTables` or the `masterTable` |  
| `relationKeys` | List[[RelationKey](#relationkey)] | Required | The names of the relation keys (columns) of the tables related |  
| `conditions` | List[[Condition](#condition), [Regex](#regex)] | Optional | A list of conditions to apply as filters |  
| `fields` | List[[TableAttribute](#tableattribute)] | Optional | List of the mapping between the attributes of the resource and the fields in the database |