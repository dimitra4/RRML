# YAML Examples

This page provides practical YAML examples that demonstrate how to define resources, mappings, and query behavior using the RRMS specification.  
Each scenario illustrates a common use case, starting with simple one-to-one mappings and gradually introducing more complex structures with additional tables, joins, and expressions.


## Simple Case Scenarios


### Mapping with a single database table

The master table is `EVENT`, with no `additionalTables`.  
The resource represents the retrieval of events from the Data Acquisition system. 

**Resource YAML**

```yaml
resource:
  resource_name: "daqevent"
  version: "1.0.0"
  hasMeta: "true"
  fields:
    - name: "eventid"
      type: "long"
      isKey: true
      meta:
        title: "Event id"
        description: "The id of the event"
        searchable: true
        sortable: true
    - name: "datetime_field"
      type: "datetime"
      meta:
        title: "Event datetime"
        description: "The datetime that the event occured"
        searchable: true
        sortable: true
    - name: "display"
      type: "boolean"
      meta:
        title: "display"
        description: "Event display"
        searchable: true
        sortable: true  
    - name: "message"
      type: "string"
      meta:
        title: "Event message"
        description: "The message of the event with all details"
        searchable: true
        sortable: true
    - name: "status"
      type: "integer"
      meta:
        title: "Event status"
        description: "The status of the event"
        searchable: true
        sortable: true       
```

**ResourceToDbMapper YAML**

```yaml
resourceToDbMapper:
  resource_name: "daqevent"
  masterTable: "event"
  dbSchema: "daq_expert"
  fields:
    - attNamedb: "ID"
      attNameResource: "eventid"
    - attNamedb: "INSERT_DATETIME"
      attNameResource: "datetime_field"
    - attNamedb: "DISPLAY"
      attNameResource: "display"
    - attNamedb: "MESSAGE"
      attNameResource: "message"
    - attNamedb: "EVENT_STATUS"
      attNameResource: "status"
  defaultSort:
    fields:
      - "eventid"
    order: "asc"
    nulls: "last"
  pagination: "enabled"
  rowCounting: "enabled"
```

---

### Mapping with two database tables

The master table is `ERAS` and `additionalTables` `RUNS`.  
The resource retrieves eras along with their first and last run numbers and corresponding times. 

**Resource YAML**

```yaml
---
resource:
  resource_name: "era"
  version: "1.0.0"
  hasMeta: true # include meta 
  fields:
    - name: "name"
      type: "string"
      isKey: true # identifier of the resource
      meta:
        description: "Era name"
        searchable: true
        sortable: true
    - name: "start_time"
      type: "datetime"
      meta:
        title: "Start time first run"
        description: "Time when the first run of this era period was started"
        searchable: true
        sortable: true
    - name: "end_time"
      type: "datetime"
      meta:
        title: "Stop time last run"
        description: "Time when the last run of this era period was stopped"
        searchable: true
        sortable: true
    - name: "start_run"
      type: "integer"
      meta:
        title: "First run"
        description: "First run number of this era period"
        searchable: true
        sortable: true
    - name: "end_run"
      type: "integer"
      meta:
        title: "Last run"
        description: "Last run number of this era period"
        searchable: true
        sortable: true
```

**ResourceToDbMapper YAML**

```yaml
masterTable: &masterTable "eras"

resourceToDbMapper:
  resource_name: "era"
  masterTable: "eras"
  dbSchema: "oms"
  fields: 
    - attNamedb: "name"
      attNameResource: "name"
  additionalTables:
    - namedb: "runs"
      dbSchema: "oms"
      relation: "asSubselect"
      relationTable: *masterTable
      relationKeys: 
        - tableKey: "era_id" 
      fields: 
        - attNamedb: "run_number"
          function: 
            name: "max"
          attNameResource: "end_run"
        - attNamedb: "run_number"
          function: 
            name: "min"
          attNameResource: "start_run"
        - attNamedb: "stop_time"
          function: 
            name: "max"
          attNameResource: "end_time"
          sort:
            by: "run_number"
            type: "dense_rank"
            order: "asc"
        - attNamedb: "start_time"
          function: 
            name: "min"
          attNameResource: "start_time"
          sort:
            by: "run_number"
            type: "dense_rank"
            order: "asc"
  defaultSort:
      fields: ["name"]
      order: "asc"
      nulls: "last"
  pagination: "disabled"
  rowCounting: "disabled"
```

## Complex Case Scenarios

These examples go beyond direct column mappings.  
They include derived columns, computed expressions, and the use of functions to transform or aggregate data.

### Expressions, functions and nested ones

The exmaple resembles the **FILL** resource, which is the fill of protons happening in the LHC for collisions. 
There some attributes with direct mapping to database columns and some, such as the `duration_total` that is a derived column, a subtract expression betwwen two columns from the master table `FILLS`.

**Resource YAML**


**ResourceToDbMapper YAML**

```yaml
masterTable: &masterTable "fills"

resourceToDbMapper:
  resource_name: "fill"
  masterTable: "fills"
  dbSchema: "cms_oms"
  primaryKey: "fill_number"
  fields: 
    - attNamedb: "fill_number"
      attNameResource: "fill_number"
    - attNameResource: "duration_total"
      expression:
        operator: "subtract"
        left: {table: "fills", column: "stop_time"}
        right: {table: "fills", column: "start_time"}
    - attNameResource: "efficiency_lumi"
      expression: 
        operator: "divide"
        left:
            operator: "multiply"
            left: 100
            right: {table: "fills", column: "recorded_lumi"}
        right: {table: "fills", column: "delivered_lumi"}
  additionalTables:
    - namedb: "downtimes"
      dbSchema: "cms_oms"
      relation: "asSubselect"
      relationTable: *masterTable
      relationKeys:
        - tableKey: "start_fill_number" 
          targetKey: "fill_number"
      conditions:
        - column: "stable_beams"  
          operator: "eq"
          value: 1                   
        - column: "enabled" 
          operator: "eq"
          value: 1      
      fields: 
        - attNameResource: "downtime" 
          function: 
            name: "sum" 
            params:
              - function: 
                  name: "round"
                  params:
                    - operator: "multiply"
                      left: 
                        operator: "subtract"
                        left: {table: "downtimes", column: "stop_time"}
                        right: {table: "downtimes", column: "start_time"}    
                      right: 150 
    - namedb: "fill_stable_beams"
      dbSchema: "cms_oms"
      relation: "leftJoin"
      relationTable: *masterTable
      relationKeys:
        - tableKey: "fill_number"
      conditions:
        - column: "stable_beams_event"   # Different names
          operator: "eq"
          value: 1                         # string, bool, number
      fields: 
        - attNamedb: "start_time"
          attNameResource: "start_stable_beam"
        - attNamedb: "end_time"
          attNameResource: "end_stable_beam"
        - attNameResource: "duration"
          expression:
            operator: "subtract"
            left: {table: "fill_stable_beams", column: "end_time"}
            right: {table: "fill_stable_beams", column: "start_time"}
        - attNamedb: "to_ready_time"
          attNameResource: "to_ready_time"
        - attNamedb: "to_tracker_ready"
          attNameResource: "to_tracker_ready_time"
        - attNamedb: "dump_ready_to_dump_time"
          attNameResource: "dump_ready_to_dump_time"
        - attNamedb: "to_dump_ready_time"
          attNameResource: "to_dump_ready_time"
        - attNameResource: "stable_beams"
          case_expression: 
            - when: { column: "start_time", operator: "isnot", value: "null"}
              then: 1
    - namedb: "runs"
      dbSchema: "cms_oms"
      relation: "asSubselect"
      relationTable: *masterTable
      relationKeys:
        - tableKey: "fill_number"
      fields: 
        - attNamedb: "b_field"
          attNameResource: "b_field"
          function: 
            name: "avg"
    - namedb: "scaling_info"
      dbSchema: "cms_oms"
      relation: "leftJoin"
      relationTable: *masterTable
      relationKeys:
        - tableKey: "scale_id"
      fields:
        - attNameResource: "delivered_lumi_stablebeams"
          expression: 
            operator: "multiply" 
            left: 
              function: 
                name: "CMS_OMS_AGG.data_summary.get_fill_delivered_lumi"
                params: [{table: "fills", column: "fill_number"}] # optional
            right: {table: "scaling_info", column: "integrated_lumi_scale_factor"}
  defaultSort:
      fields: ["fill_number"]
      order: "desc"
      nulls: "last"
  pagination: "enabled"
  rowCounting: "disabled"
```

### Grouping