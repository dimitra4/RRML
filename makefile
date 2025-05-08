# .PHONY commands makefile to treat docs serve clean as phony targets, just tasks
# not real files in project
.PHONY: docs serve clean 

# Generate documentation from Pydantic models
docs:
	source venv/bin/activate && python generate_docs.py

# Serve the documentation locally
serve:
	source venv/bin/activate && mkdocs serve

# Optional: Clean generated markdown files
clean:
	rm -f docs/*.md
