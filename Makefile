SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

PYTEST_K ?= ""
PYTEST_MARKERS ?= ""


first: help


all: npm-build pkg  ## Build JS and Python


# ------------------------------------------------------------------------------
# Python

env:  ## Create Python env
	cd $(CURDIR)/python; poetry install --with dev --with test --with docs


pkg:  ## Build package
	cd $(CURDIR)/python; poetry build


check:  ## Check linting
	cd $(CURDIR)/python; isort . --check-only --diff
	cd $(CURDIR)/python; black . --check
	cd $(CURDIR)/python; flake8


fmt:  ## Format source
	cd $(CURDIR)/python; isort .
	cd $(CURDIR)/python; black .


test-%:  ## Run tests
	cd $(CURDIR)/python; pytest -k $(PYTEST_K) -m $(subst test-,,$@)


test-all:  ## Run all tests
	cd $(CURDIR)/python; pytest -k $(PYTEST_K) -m $(PYTEST_MARKERS)


report:  ## Generate coverage reports
	cd $(CURDIR)/python; coverage xml
	cd $(CURDIR)/python; coverage html


upload-pypi:  ## Upload package to PyPI
	cd $(CURDIR)/python; twine upload dist/*.tar.gz


cleanpython:  ## Clean Python build files
	cd $(CURDIR)/python; rm -rf .pytest_cache dist
	cd $(CURDIR)/python; rm -f .coverage coverage.xml
	find . -type f -name '*.py[co]' -delete
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .ipynb_checkpoints -exec rm -rf {} +


resetpython: cleanpython  ## Reset Python
	cd $(CURDIR)/python; rm -rf .venv


example:  ## Dev: Run nbconvert on one example
	cd $(CURDIR)/examples && ILLUSIONIST_DEV_MODE=1 jupyter nbconvert widget-gallery.ipynb --to illusionist


# ------------------------------------------------------------------------------
# Javascript

npm-install:  ## JS: Install dependencies
	cd $(CURDIR)/js; npm install
npm-i: npm-install


npm-build:  ## JS: Build
	cd $(CURDIR)/js; npm run build:all


npm-dev:  ## JS: Build dev mode
	cd $(CURDIR)/js; npm run dev


npm-publish:  ## JS: Publish to NPM
	cd $(CURDIR)/js; npm version
	cd $(CURDIR)/js; npm publish


cleanjs:  ## JS: Clean build files
	cd $(CURDIR)/js; npm run clean
	rm -rf $(CURDIR)/python/illusionist/templates/illusionist/assets/*.js*
	rm -rf $(CURDIR)/python/illusionist/templates/illusionist/assets/*.css*


resetjs:  ## JS: Reset
	cd $(CURDIR)/js; npm run reset


# ------------------------------------------------------------------------------
# Docs

docs:  ## Docs: Build
	$(MAKE) docs-examples-html
	mkdocs build
	$(MAKE) docs-example-exec-nbs
.PHONY: docs


docs-serve:  ## Docs: Serve
	mkdocs serve


docs-examples-html:  ## Docs: Convert examples to HTML
	cd $(CURDIR)/examples && jupyter nbconvert *.ipynb	--output-dir=$(CURDIR)/docs/examples/	--to illusionist


docs-example-exec-nbs:  ## Docs: Execute examples and output them into docs
	cd $(CURDIR)/examples && jupyter nbconvert *.ipynb	--output-dir=$(CURDIR)/site/examples/notebooks	--to illusionist-nb	--execute


examples-clear-output:  ## Clear output of notebooks
	cd $(CURDIR)/examples && jupyter nbconvert */*.ipynb --clear-output --inplace


serve-examples:  ## Docs: Serve examples
	cd $(CURDIR)/examples && python -m http.server


# ------------------------------------------------------------------------------
# Other

cleanall: cleanjs cleanpython  ## Clean everything
	rm -rf site
	rm -f $(CURDIR)/examples/*.html
	rm -f $(CURDIR)/docs/examples/*.html


help:  ## Show this help menu
	@grep -E '^[0-9a-zA-Z_-]+:.*?##.*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?##"; OFS="\t\t"}; {printf "\033[36m%-30s\033[0m %s\n", $$1, ($$2==""?"":$$2)}'

