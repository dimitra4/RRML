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
    """
    The *MetaData* provides descriptive and behavioral information for a resource attribute.
    It can provide a human-readable title and description, indicate whether the attribute supports filtering
    and sorting in queries, and specify any associated measurement units.

    Together, these metadata properties enhance both API usability and
    query capabilities without altering the structural definition of the attribute itself.
    """
    
    title: Optional[str] = None
    description: Optional[str] = None
    searchable: bool = Field(
        description="Indicates whether this attribute can be used in query filters",
        default=None
    )
    sortable: bool = Field(
        description="Indicates whether this attribute can be used to order query results",
        default=None
    )
    units: Optional[SanitizedStr] = Field(
        description="Unit of the attribute, as defined in the [*supported_units*](#SupportedTypesandUnits) YAML file",
        default=None
    )


class Attribute(TypoDetectingModel):
    """
    The *Attribute* defines a single field of a Resource. Each attribute has
    a name and type, may be marked as the key identifier of the resource, and
    can optionally include additional metadata for documentation and query
    behavior.
    """
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
    """
    The *Resource* model defines the representation of a domain entity exposed through the API.

    - Each resource has a unique `resource_name` and may include a `version` for documentation and lifecycle tracking.
    - A resource is composed of a list of `Attribute` elements. Each attribute carries:
        - **Structural metadata** (e.g. its name, description, units).
        - **Behavioral flags** that determine how it can be used in the API and in internal query logic (e.g. filtering, sorting, or key fields).

    Together, these properties ensure that a Resource can be consistently documented, validated, and mapped to underlying database entities.
    """
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
    def validate_resource_model(cls, model_instance):
        """
        Perform post-validation checks on a Resource definition. This validator runs **after** field-level validation and case normalization.
        It ensures that every Resource has a proper identifier field defined.

        Specifically, it enforces:
        
        1. **Key field requirement**
            - At least one attribute in `resource.fields` must have `isKey=True`.
            - This key field serves as the unique identifier of the Resource.
            - Composite identifiers are also supported by marking multiple attributes with `isKey=True`.


        If no key field is found, a ValueError is raised, clearly listing the issue.

        This safeguard guarantees that every Resource defined in the specification
        can be uniquely identified, which is a prerequisite for consistent mapping
        to database entities and for stable API resource behavior.
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

