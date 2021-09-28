SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

PYTEST_K ?= ""
TEST_MARKERS ?= ""


first: help


all: npm-build build-python  ## Build JS and Python package


# ------------------------------------------------------------------------------
# Python

env:  ## Create Python env
	cd $(CURDIR)/python; poetry install


build-python:  ## Build package
	cd $(CURDIR)/python; poetry build


upload-pypi:  ## Upload package to PyPI
	cd $(CURDIR)/python; twine upload dist/*.tar.gz


upload-test:  ## Upload package to test PyPI
	cd $(CURDIR)/python; twine upload --repository test dist/*.tar.gz


check:  ## Check linting
	cd $(CURDIR)/python; isort . --check-only --diff
	cd $(CURDIR)/python; black . --check
	cd $(CURDIR)/python; flake8


fmt:  ## Format source
	cd $(CURDIR)/python; isort .
	cd $(CURDIR)/python; black .


test:  ## Run tests
	cd $(CURDIR)/python; pytest -k $(PYTEST_K) -m $(TEST_MARKERS)


report:  ## Generate coverage reports
	cd $(CURDIR)/python; coverage xml
	cd $(CURDIR)/python; coverage html


cleanpython:  ## Clean Python build files
	cd $(CURDIR)/python; rm -rf build dist htmlcov .pytest_cache test-results .eggs
	cd $(CURDIR)/python; rm -f .coverage coverage.xml illusionist/_generated_version.py
	find . -type f -name '*.py[co]' -delete
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .ipynb_checkpoints -exec rm -rf {} +


# ------------------------------------------------------------------------------
# JS

npm-i: npm-install
npm-install:  ## Install JS dependencies
	cd $(CURDIR)/js/; npm install


npm-build:  ## Build JS
	cd $(CURDIR)/js/; npm run build:all


npm-dev:  ## Build JS with watch
	cd $(CURDIR)/js/; npm run dev


npm-publish:  ## Publish NPM
	cd $(CURDIR)/js/; npm version
	cd $(CURDIR)/js/; npm publish


cleanjs:  ## Clean JS build files
	rm -rf $(CURDIR)/python/share/jupyter/nbconvert/templates/illusionist/static/dist/*.js
	rm -rf $(CURDIR)/python/share/jupyter/nbconvert/templates/illusionist/static/dist/*.js.map
	rm -rf $(CURDIR)/python/share/jupyter/nbconvert/templates/illusionist/static/dist/*.css
	rm -rf $(CURDIR)/python/share/jupyter/nbconvert/templates/illusionist/static/dist/*.css.map
	rm -rf $(CURDIR)/python/share/jupyter/nbconvert/templates/illusionist/static/dist/*.html
	rm -rf $(CURDIR)/python/share/jupyter/nbconvert/templates/illusionist/static/dist/*.woff
	rm -rf $(CURDIR)/python/share/jupyter/nbconvert/templates/illusionist/static/dist/*.woff2
	rm -rf $(CURDIR)/python/share/jupyter/nbconvert/templates/illusionist/static/dist/*.eot
	rm -rf $(CURDIR)/python/share/jupyter/nbconvert/templates/illusionist/static/dist/*.ttf
	rm -rf $(CURDIR)/python/share/jupyter/nbconvert/templates/illusionist/static/dist/*.svg
	cd $(CURDIR)/js/; rm -rf .cache dist lib


# ------------------------------------------------------------------------------
# Docs

docs:  ## Build docs
	# $(MAKE) docs-examples-html
	mkdocs build
	# $(MAKE) docs-example-exec-nbs
.PHONY: docs


serve-docs:  ## Serve docs
	mkdocs serve


docs-examples-html:  ## Docs: Examples to HTML
	cd $(CURDIR)/examples && jupyter nbconvert *.ipynb	--output-dir=$(CURDIR)/docs/examples/	--to illusionist


docs-example-exec-nbs:  ## Docs: Execute example notebooks and output them into docs
	cd $(CURDIR)/examples && jupyter nbconvert *.ipynb	--output-dir=$(CURDIR)/site/examples/notebooks	--to illusionist-nb	--execute


serve-examples:  ## Serve examples
	cd $(CURDIR)/examples && python -m http.server


example:  ## Dev: Run nbconvert on one example
	cd $(CURDIR)/examples && ILLUSIONIST_DEV_MODE=1 jupyter nbconvert widget-gallery.ipynb --to illusionist


# ------------------------------------------------------------------------------
# Other

reset: cleanall  ## Same as cleanall
cleanall: cleanpython cleanjs  ## Clean everything
	rm -rf site $(CURDIR)/docs/examples/*.html
	cd $(CURDIR)/examples/; rm -rf *.html
	cd $(CURDIR)/python/; rm -rf *.egg-info
	cd $(CURDIR)/js/; rm -rf node_modules


help:  ## Show this help menu
	@grep -E '^[0-9a-zA-Z_-]+:.*?##.*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?##"; OFS="\t\t"}; {printf "\033[36m%-30s\033[0m %s\n", $$1, ($$2==""?"":$$2)}'

