## Function



**Attributes:**

| Name | Type | Status | Description | Constraints |
|:-----|:-----|:-------|:------------|:------------|
| `name` | str | Optional | Fully qualified name of the db function to call or any other built-in sql function | Examples: min, max, count, avg, sum, round, upper, trim |
| `params` | List[ForwardRef('Expression'), ForwardRef('FunctionCall'), [DBColumnReference](#dbcolumnreference), str, int, float, bool] | Optional | Optional parameters to pass to the function |  |
| `distinct` | bool | Optional | Distinct inside the function | Examples: C, O, U, N, T, (, D, I, S, T, I, N, C, T,  , v, a, l, u, e, ) |



                          


                          
{% include-markdown "DBColumnReference.md" %}