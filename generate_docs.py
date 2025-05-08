import os
import importlib
import inspect
import re
from typing import Type, List, Any, get_origin, get_args, Union, Literal
from pydantic import BaseModel
from jinja2 import Template

# ==== CONFIG ====
BASE_MODULE = "pydantic_models"  # models folder name
BASE_PATH = "pydantic_models"    # models folder path
OUTPUT_DIR = "docs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==== TEMPLATES ====

MODEL_TEMPLATE = Template("""
## {{ model_name }}

{{ model_description or '' }}

**Attributes:**

| Name | Type | Status | Description | Constraints |
|:-----|:-----|:-------|:------------|:------------|
{% for field in fields -%}
| `{{ field.name }}` | {{ field.type }} | {% if field.status%}Required{% else %}Optional{% endif %} | {{ field.description }} | {{ field.constraints }} |
{% endfor %}

{% if validators %}
### Validators

{% for validator in validators %}
- **{{ validator.name }}**: {{ validator.description }}
{% endfor %}
{% endif %}
""")


INDEX_TEMPLATE = Template("""
# Resource and Query Builder Specification                  

## Models

{% for model in models %}
- [{{ model.name }}](#{{model.name.lower()}})
{% endfor %}
                          
{% for model in models %}
{% raw %}{% include-markdown "{% endraw %}{{ model.filename }}{% raw %}" %}{% endraw %}        
{% endfor %}
""")

# ==== HELPERS ====

def clean_annotation(annotation: Any) -> tuple[str, bool, str]:
    origin = get_origin(annotation)
    args = get_args(annotation)
    print(f"annotation {annotation} origin {origin} args {args}")

    # Handle Optional (which is Union[X, None])
    if origin is Union and type(None) in args:
        non_none = [a for a in args if a is not type(None)][0]
        inner_str, is_model, required_field = clean_annotation(non_none)
        return f"{inner_str}", is_model, required_field

    # Handle List[T] or list[T]
    if origin in {list, List}:
        inner_str, is_model, required_field = clean_annotation(args[0])
        return f"List[{inner_str}]", is_model, required_field

    if origin is Literal:
        return f"Literal[{', '.join(args)}]", False, True

    # Handle Union[A, B] (non-optional)
    if origin is Union:
        parts = []
        is_model = False
        for arg in args:
            part_str, is_part_model, required_field = clean_annotation(arg)
            parts.append(part_str)
            if is_part_model:
                is_model = True
        return f"{', '.join(parts)}", is_model, required_field

    # Base case — no args, just a type like str, int, or a model
    if hasattr(annotation, "__name__"):  # like str, int, bool, Resource
        name = annotation.__name__
        is_model = name not in {"str", "int", "bool", "float", "list", "dict"}
        if is_model:
            name = f"[{name}]({name}.md)"
        return name, is_model, is_model

    # Fallback (for weird types)
    typename = str(annotation).replace("typing.", "").split(".")[-1]
    return typename, typename[0].isupper(), typename[0].isupper()


def extract_fields(model: Type[BaseModel]) -> List[dict]:
    fields = []
    for field_name, field_obj in model.model_fields.items():
        # print(f"model_fields{model.model_fields.items()}")
        print(f"field_name {field_name}")
        annotation, is_model, required_field = clean_annotation(field_obj.annotation)
        print(annotation, is_model, required_field)
        desc = field_obj.description or ""
        extras = []

        if getattr(field_obj, 'examples', None):
            examples = ', '.join(map(str, field_obj.examples))
            extras.append(f"Examples: {examples}")
        if getattr(field_obj, 'pattern', None):
            extras.append(f"Pattern: `{field_obj.pattern}`")
        if getattr(field_obj, 'min_items', None):
            extras.append(f"Min items: {field_obj.min_items}")

        fields.append({
            "name": field_name,
            "type": annotation,
            "status": required_field,
            "description": desc,
            "constraints": "<br>".join(extras) if extras else ""
        })
    return fields

def extract_validators(model: Type[BaseModel]) -> List[dict]:
    validators = []
    for name, func in inspect.getmembers(model, predicate=inspect.isfunction):
        if "@model_validator" in inspect.getsource(func):
            doc = inspect.getdoc(func) or "Custom model validation."
            validators.append({"name": name, "description": doc})
    return validators

def render_model(model: Type[BaseModel]) -> dict:
    model_name = model.__name__
    fields = extract_fields(model)
    validators = extract_validators(model)

    markdown = MODEL_TEMPLATE.render(
        model_name=model_name,
        model_description=model.__doc__,
        fields=fields,
        validators=validators
    )

    filename = f"{model_name}.md"
    with open(os.path.join(OUTPUT_DIR, filename), "w") as f:
        f.write(markdown.strip())
    print(f"Generated {filename}")

    return {"name": model_name, "filename": filename}

def render_index(models_info: List[dict]):
    index_md = INDEX_TEMPLATE.render(models=models_info)
    with open(os.path.join(OUTPUT_DIR, "index.md"), "w") as f:
        f.write(index_md.strip())
    print(f"Generated index.md")

def discover_modules(base_module: str, base_path: str) -> List[str]:
    """Auto-discover all .py modules inside base_path."""
    modules = []
    for filename in os.listdir(base_path):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            modules.append(f"{base_module}.{module_name}")
    return modules

def find_pydantic_models(module) -> List[Type[BaseModel]]:
    models = []
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if issubclass(obj, BaseModel) and obj.__module__ == module.__name__:
            models.append(obj)
    return models

# ==== MAIN ====

def main():
    module_names = discover_modules(BASE_MODULE, BASE_PATH)
    print(module_names)

    models_info = []
    for module_name in module_names:
        mod = importlib.import_module(module_name)
        models = find_pydantic_models(mod)
        
        for model in models:
            models_info.append(render_model(model))
            
    print(models_info)  

    render_index(models_info)

if __name__ == "__main__":
    main()
