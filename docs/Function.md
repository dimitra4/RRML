## Function


Represents a database function or built-in SQL function call.
A `Function` defines the fully qualified name of the function, along with any optional parameters and whether the call should apply `DISTINCT`.

**Example YAML**

```yaml
function: 
    name: "count"
    distinct: true
```
corresponds to:
```sql
COUNT(DISTINCT column_name)
```

                          
---
**Attributes:**

| Name | Type | Status | Description | Examples |
|:-----|:-----|:-------|:------------|:------------|
| `name` | str | Required | Fully qualified name of the db function to call or any other built-in sql function | min, max, count, avg, sum, round, upper, trim 
| `params` | List[ForwardRef('Expression'), ForwardRef('FunctionCall'), [DBColumnReference](#dbcolumnreference), str, int, float, bool] | Optional | Optional parameters to pass to the function |  
| `distinct` | bool | Optional | Distinct inside the function |