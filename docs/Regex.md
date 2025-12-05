## Regex


Represents a **regular expression transformation** applied to a column.
A `Regex` extracts or validates parts of a string column using SQL regex
functions such as `REGEXP_SUBSTR`.

                          
---
**Attributes:**

| Name | Type | Status | Description | Examples |
|:-----|:-----|:-------|:------------|:------------|
| `column` | str | Required | The name of the column to which the regular expression will be applied. It must match one of the defined relation keys |  
| `pattern` | str | Required | The regular expression pattern |  
| `groups` | List[int] | Required | The grouping where the pattern will be applied |