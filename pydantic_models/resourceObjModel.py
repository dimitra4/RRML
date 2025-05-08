import re
from .enum import FieldType

from typing import (
    Literal,
    Optional,
    List,
    Any,
    Annotated
)
from pydantic import (
    BaseModel,
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

class MetaData(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    searchable: Optional[bool]
    sortable: Optional[bool]
    units: Optional[SanitizedStr] = None


class Attribute(BaseModel):
    name: SanitizedStr = Field(
        description="Name of the attribute of the resource",
        examples=["id", "start_time", "run_number"]
    )
    type: FieldType = Field(
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

class Resource(BaseModel):
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

    @model_validator(mode="before")
    @classmethod
    def validate_fields(cls, v: dict[str, Any]) -> dict[str, Any]:
        errors = []
        fields = v.get("fields", [])
        if not fields:
            raise ValueError("The key 'fields' must be provided and must contain at least one attribute.")

        has_key_field = False

        for idx, field in enumerate(fields):
            # Ensure 'name' is present
            if 'name' not in field:
                errors.append(f"fields[{idx}]: The 'name' attribute is missing. ")

            # Ensure 'type' is present
            if 'type' not in field:
                errors.append(f"fields[{idx}]: The 'type' attribute is missing.")

            if field.get('isKey') is True:
                has_key_field = True

        if not has_key_field:
            errors.append(f"At least one attribute from 'fields' must have isKey=true.")
        
        # Raise all errors at once
        if errors:
            raise ValueError("Validation errors:\n" + "\n".join(errors) + "\n")

        return v

    
class ResourceMappingSpec(BaseModel):
    resource: Resource = Field(
        description="The resource object containing metadata and fields.",
        validation_alias='resource'
    )

# valid_instance = Attribute(name="John@Doe#123!", type="string" )
# print(valid_instance)