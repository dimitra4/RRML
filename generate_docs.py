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
                          
{% for field in fields -%}
{% set safe = field.type|default('', true) -%}
{% set before_link = safe.split('](#')[0] -%}
{% set name = before_link.rsplit('[', 1)[-1] -%}
{% if field.is_model and name %}
{% if name in ('ArithmeticOperator', 'ComparisonOperator')%}    
{% raw %}{% include-markdown "{% endraw %}enum.md{% raw %}" %}{% endraw %} 
{% else %}                          
{% raw %}{% include-markdown "{% endraw %}{{ name }}.md{% raw %}" %}{% endraw %} 
{% endif %}
{% endif %}
{% endfor %}
""")


INDEX_TEMPLATE = Template("""
# RESTful Resource Mapping Specification (RRMS) 

The **RESTful Resource Mapping Specification (RRMS)** is a lightweight, declarative language for defining RESTful API resources and their mappings to relational databases.  

Instead of writing boilerplate code for every new endpoint, developers and domain experts can describe resources in **human-readable YAML files**, including:

- Resource attributes and identifiers  
- Database mappings and joins  
- Query logic, functions, and aggregations  
- Validation constraints  

These specifications are automatically validated and transformed into executable code through a **template-based code generation pipeline**. The result is a set of fully functional API components—resources, repositories, mappers, and query builders—aligned with the existing backend.

---

## Why use RRMS?

- **Reduce boilerplate**: eliminate repetitive coding of endpoints.  
- **Consistency by design**: endpoints follow the same structure and rules.  
- **Expressiveness**: model simple to complex query logic in a declarative way.  
- **Faster onboarding**: new developers or domain experts can contribute without mastering backend frameworks.  
- **Flexibility**: templates can target different runtimes (Java today, Python/FastAPI or others tomorrow).  

---

## Who is this for?

- **API developers** who want to speed up endpoint creation.  
- **Domain experts** who can describe data models without writing code.  
- **Teams** aiming for maintainability, scalability, and alignment across APIs.  

---

## How it works (at a glance)

1. **Write** YAML files describing resources and their mappings.  
2. **Validate** them against the RRMS metamodel (Pydantic). They must conform to the main Pydantic object models  
3. **Generate** backend code automatically via Jinja templates.  
4. **Deploy** the generated classes as working REST endpoints.                

## Main Pydantic Object Models

- [Resource](#resource)
- [ResourceToDbMapper](#resourcetodbmapper)
                          
""")
# {% for model in models %}
# {% raw %}{% include-markdown "{% endraw %}{{ model.filename }}{% raw %}" %}{% endraw %}        
# {% endfor %}

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
            anchor = name.lower()
            name = f"[{name}](#{anchor})"
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
            "is_model": is_model,
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
        print(models)
        
        for model in models:
            FULL_NAME = f"{model.__module__}.{model.__name__}"
            if FULL_NAME not in {
                # "pydantic_models.queryBuilderObjModel.AdditionalTable",
                # "pydantic_models.queryBuilderObjModel.Function",
                "pydantic_models.queryBuilderObjModel.ResourceToDbMappingSpec",
                "pydantic_models.resourceObjModel.ResourceMappingSpec"
            }:
                print(model)
                models_info.append(render_model(model))
            
    print(models_info)  

    render_index(models_info)

if __name__ == "__main__":
    main()
