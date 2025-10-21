import re
from .enum import FieldType
from .typoDetectingModel import TypoDetectingModel

from typing import (
    Literal,
    Optional,
    List,
    Any,
    Annotated
)
from pydantic import (
    Field,
    field_validator,
    model_validator,
    ValidationInfo,
    AfterValidator
)

# todo raise error if there not at all in the model instance the isKey field ** done
# todo add attr spec_version and validate

# Define a reusable validator for cleaning strings
def sanitize_string(value: str) -> str:
    """Sanitizes a string by replacing special characters with an underscore."""
    cleaned_value = re.sub(r'[^a-zA-Z0-9_-]', '', value)
    if cleaned_value != value:
        print(f"Sanitized input: {value} -> {cleaned_value}")
    return cleaned_value

# Create an Annotated type with the validator
SanitizedStr = Annotated[str, AfterValidator(sanitize_string)]

class MetaData(TypoDetectingModel):
    title: Optional[str] = None
    description: Optional[str] = None
    searchable: bool
    sortable: bool
    units: Optional[SanitizedStr] = None


class Attribute(TypoDetectingModel):
    name: SanitizedStr = Field(
        description="Name of the attribute of the resource",
        examples=["id", "start_time", "run_number"]
    )
    type: str= Field(
        description="The data type of the attribute of the resource according to the standardized mapping_types YAML file"
    ) 
    isKey: Optional[bool] = Field(
        description="Explicitly determine true if the attribute is the actual identifier of the resource",
        default=None
    )
    meta: Optional[MetaData] = Field(
        description="The meta data of the attribute",
        default=None,
    )

class Resource(TypoDetectingModel):
    resource_name: str = Field(
        description="The name of the resource. All classes will be named using this name",
        pattern=r'^[a-zA-Z0-9_]+$',  # Allows letters, digits, and underscores (no special characters)
        examples=["era", "fill", "resource_1", "data2024"]
    )
    version: str = Field(
        description="Release of a project, marked by a version number ",
        examples=["1.0.0"]
    )
    hasMeta: Optional[bool] = None
    fields: List[Attribute] = Field(
        description="List of the attributes of the resource",
        min_items=1
    )

    @model_validator(mode="after")
    @classmethod
    def validate_fields(cls, model_instance):
        """
        Runs AFTER case correction and field validation for business logic validation
        """
        errors = []
        
        fields = model_instance.fields
        has_key_field = False
 
        for idx, field in enumerate(fields):                   
            # Check for key field
            if field.isKey is True:
                has_key_field = True
        
        if not has_key_field:
            errors.append("At least one field must have isKey=true, that represents the identifier of the Resource")
        
        if errors:
            error_message = f"Resource validation failed with {len(errors)} error(s):\n"
            error_message += "\n".join(f"  • {error}" for error in errors)
            raise ValueError(error_message)
        
        return model_instance

    
class ResourceMappingSpec(TypoDetectingModel):
    resource: Resource = Field(
        description="The resource object containing metadata and fields.",
        validation_alias='resource'
    )

