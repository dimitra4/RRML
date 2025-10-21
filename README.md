# RQB

The RQB acronym stands for **Resource and Query Builder** Specification. This project is dedicated to explain the process of creating my documented-focused site with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)

<div align="center">
  <img src="/docs/assets/images/rqb_rocket.png" alt="RQB Logo" width="600">
</div>

## Prerequisites

These are the *prerequisites* you’ll need to have installed if you want to run this project:

- [Python](https://www.python.org/downloads/) 
    - [pip](https://pip.pypa.io/en/stable/installation/) - the Python package manager (included by default in Python 3.4 and later)
    - [pyyaml](https://pypi.org/project/PyYAML/) - a Python YAML parser and emitter
    - [pydantic](https://docs.pydantic.dev/latest/) - a Python data validation library
- [Jinja](https://jinja.palletsprojects.com/en/stable/) - a web template engine that allows writing code similar to Python syntax. 
    - [Install Jinja2](https://jinja.palletsprojects.com/en/stable/intro/#installation) - most recent Jinja version
- [Visual Studio Code](https://code.visualstudio.com/) - or any other IDE of your choice

<br>

### Tutorials

Material for MkDocs:
- [mkdocs-material documentation](https://jameswillett.dev/getting-started-with-material-for-mkdocs/#collapsible-admonitions)
- [mkdocs-material Youtube video](https://www.youtube.com/watch?v=xlABhbnNrfI)

<br><br>

Go to Visual Studio settings and add the below to the json file.
This is YAML validation for the mkdocs material theme and functionality.

```
  "yaml.schemas": {
    "https://squidfunk.github.io/mkdocs-material/schema.json": "mkdocs.yml"
  },
  "yaml.customTags": [
    "!ENV scalar",
    "!ENV sequence",
    "!relative scalar",
    "tag:yaml.org,2002:python/name:material.extensions.emoji.to_svg",
    "tag:yaml.org,2002:python/name:material.extensions.emoji.twemoji",
    "tag:yaml.org,2002:python/name:pymdownx.superfences.fence_code_format"
  ]
```

## Run

```
cd spec_site
source venv/bin/activate    # activate virtual env
mkdocs serve
```
