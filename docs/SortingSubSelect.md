## SortingSubSelect



**Attributes:**

| Name | Type | Status | Description | Constraints |
|:-----|:-----|:-------|:------------|:------------|
| `by` | str | Optional | The field name to sort by, e.g., 'run_number'. |  |
| `type` | Literal[dense_rank, rank, row_number] | Required | The sort method to use. Options include:
- 'dense_rank': Assigns ranks with no gaps in ranking values.
- 'rank': Like dense_rank but leaves gaps in the ranking sequence for ties.
- 'row_number': Assigns a unique sequential number to rows.
 |  |
| `order` | Literal[asc, desc] | Required | The direction of sorting: 'asc' for ascending, 'desc' for descending. |  |