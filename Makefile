.PHONY: lint
lint:
	pylint ./*.py

.PHONY: generate-requirements
generate-requirements:
	pip3 freeze > requirements.txt

.PHONY: install-requirements
install-requirements:
	pip3 install -r requirements.txt