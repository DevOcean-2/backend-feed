.PHONY: lint
PYLINT := .venv/bin/pylint

lint:
	pylint app/*py app/**/*.py --output-format=colorized

.PHONY: generate-requirements
generate-requirements:
	pip3 freeze > requirements.txt

.PHONY: install-requirements
install-requirements:
	pip3 install -r requirements.txt