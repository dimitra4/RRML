## ResourceToDbMapper



**Attributes:**

| Name | Type | Status | Description | Constraints |
|:-----|:-----|:-------|:------------|:------------|
| `resource_name` | str | Optional | The name of the resource. Needs to be associated with an existing resource | Examples: era, fill |
| `masterTable` | str | Optional | The name of the database's master table |  |
| `dbSchema` | str | Optional | The schema of the database's master table |  |
| `primaryKey` | str | Optional | The primary key the database's master table |  |
| `fields` | List[[TableAttribute](TableAttribute.md)] | Required | List of the mapping between the attributes of the resource and the fields in the database |  |
| `additionalTables` | List[[AdditionalTable](AdditionalTable.md)] | Required | Provides all the information about relations between the master table and other tables |  |
| `groupBy` | List[str] | Optional | Applies grouping to the db resultset |  |
| `defaultSort` | [SortedQuery](SortedQuery.md) | Required | Specifies the default sorting to the db resultset |  |
| `pagination` | Literal[enabled, disabled] | Required | Paginate the db resultset |  |
| `rowCounting` | Literal[enabled, disabled] | Required | Counting of the rows from the db resultset |  |