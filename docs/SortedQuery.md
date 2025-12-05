## SortedQuery


Represents an **ORDER BY clause** in a query.
A `SortedQuery` defines which attributes can be sorted, the sorting direction, and whether null values appear first or last.<br>
This defines the default sorting of the resource if no sorting is specified in the REST request.

**Example YAML**

```yaml
defaultSort:
  fields: ["name"]
  order: "asc"
  nulls: "last"
```

corresponds to:
```sql
ORDER BY name ASC NULLS LAST
```

                          
---
**Attributes:**

| Name | Type | Status | Description | Examples |
|:-----|:-----|:-------|:------------|:------------|
| `fields` | List[str] | Required | List of the accepted attributes to be sorted |  
| `order` | Literal[asc, desc] | Optional | Accepted order for the sorted query |  
| `nulls` | Literal[last, first] | Optional | Show nulls last or first |