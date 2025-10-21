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