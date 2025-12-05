## DBColumnReference


References a **database column** by its table and column name.
Used throughout the specification to unambiguously refer to database fields in conditions, expressions, or mappings.

**Example YAML**

```yaml
table: "eras"
column: "name"
```

corresponds to:
```sql
eras.name
```

                          
---
**Attributes:**

| Name | Type | Status | Description | Examples |
|:-----|:-----|:-------|:------------|:------------|
| `table` | str | Required | The table name of the referenced column |  
| `column` | str | Required | The name of the column being referenced. |