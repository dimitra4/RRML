## TypoDetectingModel


                          
---
**Attributes:**

| Name | Type | Status | Description | Examples |
|:-----|:-----|:-------|:------------|:------------|



### Validators


**`validate_resource_model:`**
Pre-processor for input data: corrects case variations and flags likely typos.

This validator runs **before** standard field validation. Its purpose is to
normalize input keys and catch common mistakes early, improving both
robustness and user experience.

Specifically, it:
1. Case correction:
   - Accepts field names in any case (e.g., `ResourceName`, `resourcename`)
     and maps them back to the canonical field defined in the model.

2. Typo detection:
   - Uses fuzzy matching to detect close matches to known field names.
   - If a likely match is found, raises an error with a suggestion:
     e.g., `"Unexpected field 'resouce'. Did you mean 'resource'?"`

3. Unknown field rejection:
   - If no close match is found and the field is not in the allowed exceptions
     (`java_type`, `db_type`), raises an error about the unknown field.

Returns:
    A corrected dictionary of field names → values, ready for standard validation.

Raises:
    ValueError: If unrecognized or mistyped fields are detected.