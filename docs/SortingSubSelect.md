## SortingSubSelect


Represents a **window function ordering** applied in a subselect.
A `SortingSubSelect` specifies the field, ordering method, and direction used when sorting rows with ranking functions like `RANK` or `ROW_NUMBER`.

**Example YAML**

```yaml
sort:
  by: "run_number"
  type: "dense_rank"
  order: "desc"
```
corresponds to:
```sql
DENSE_RANK() OVER (ORDER BY run_number DESC)
```

                          
---
**Attributes:**

| Name | Type | Status | Description | Examples |
|:-----|:-----|:-------|:------------|:------------|
| `by` | str | Required | The field name to sort by, e.g., 'run_number'. |  
| `type` | Literal[dense_rank, rank, row_number] | Required | The sort method to use. Options include:<br>- 'dense_rank': Assigns ranks with no gaps in ranking values.<br>- 'rank': Like dense_rank but leaves gaps in the ranking sequence for ties.<br>- 'row_number': Assigns a unique sequential number to rows.<br> |  
| `order` | Literal[asc, desc] | Required | The direction of sorting: 'asc' for ascending, 'desc' for descending. |