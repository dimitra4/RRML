## SortedQuery



**Attributes:**

| Name | Type | Status | Description | Constraints |
|:-----|:-----|:-------|:------------|:------------|
| `fields` | List[str] | Optional | List of the accepted attributes to be sorted |  |
| `order` | Literal[asc, desc] | Required | Accepted order for the sorted query |  |
| `nulls` | Literal[last, first] | Required | Show nulls last or first |  |