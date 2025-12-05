from pydantic import BaseModel, model_validator
from typing import Dict, Any
from difflib import get_close_matches

class TypoDetectingModel(BaseModel):
    class Config:
        extra = "forbid" # allow
    
    @model_validator(mode="before")
    @classmethod
    def catch_likely_typos_and_case_variations(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """
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
        """
        if not isinstance(values, dict):
            return values
            
        known_fields = set(cls.model_fields.keys())
        known_fields_lower = {field.lower(): field for field in known_fields}
        # print(f"known_fields_lower {known_fields_lower}")
        
        corrected_values = {}
        errors = []
        
        for input_field, value in values.items():
            input_field_lower = input_field.lower()
            if input_field_lower in known_fields_lower:
                correct_field = known_fields_lower[input_field_lower]
                corrected_values[correct_field] = value
        
            else:
                close_matches = get_close_matches(
                    input_field.lower(), 
                    known_fields_lower.keys(), 
                    n=1, 
                    cutoff=0.8
                )
                
                if close_matches:
                    suggestion = known_fields_lower[close_matches[0]]
                    errors.append({
                        "loc": f"{input_field}",
                        "msg": f"Unexpected field '{input_field}'. Did you mean '{suggestion}' ?",
                        "type": "value_error.possible_typo"
                    })
                elif input_field not in ('java_type', 'db_type'):
                    errors.append({
                        "loc": f"{input_field}",
                        "msg": f"Unexpected field '{input_field}'. No similar field found in the specification.",
                        "type": "value_error.unknown_field"
                    })
        
        if errors:
            raise ValueError("\n".join(str(err) for err in errors))
        
        return corrected_values
