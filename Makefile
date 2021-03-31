SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

PWD := $(shell pwd)
PYTEST_K ?= ""


first: help


build: npm-build python-build  ## Build JS and Python package


# ------------------------------------------------------------------------------
# Python

env:  ## Create dev environment
	cd $(CURDIR)/python; mamba env create


develop:  ## Install package for development
	cd $(CURDIR)/python; python -m pip install --no-build-isolation -e .


extensions:  ## Install Jupyter extensions
	jupyter labextension install @jupyter-widgets/jupyterlab-manager


python-build:  ## Build Python package (sdist)
	cd $(CURDIR)/python; python setup.py sdist


check:  ## Check linting
	cd $(CURDIR)/python; flake8
	cd $(CURDIR)/python; isort . --project jupyter_flex --check-only --diff
	cd $(CURDIR)/python; black . --check


fmt:  ## Format source
	cd $(CURDIR)/python; isort . --project jupyter-flex
	cd $(CURDIR)/python; black .


upload-pypi:  ## Upload package to PyPI
	cd $(CURDIR)/python; twine upload dist/*.tar.gz


upload-test:  ## Upload package to test PyPI
	cd $(CURDIR)/python; twine upload --repository test dist/*.tar.gz


test:  ## Run tests
	cd python && pytest -k $(PYTEST_K)


report:  ## Generate coverage reports
	cd $(CURDIR)/python; coverage xml
	cd $(CURDIR)/python; coverage html


cleanpython:  ## Clean Python build files
	cd $(CURDIR)/python; rm -rf build dist htmlcov .pytest_cache test-results .eggs
	cd $(CURDIR)/python; rm -f .coverage coverage.xml jupyter_flex/_generated_version.py
	find . -type f -name '*.py[co]' -delete
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .ipynb_checkpoints -exec rm -rf {} +


# ------------------------------------------------------------------------------
# JS

npm-build:  ## Build JS
	cd $(CURDIR)/js/; npm run build:all


npm-i: npm-install
npm-install:  ## Install JS dependencies
	cd $(CURDIR)/js/; npm install


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

.PHONY: docs
docs:  ## Build docs
	$(MAKE) docs-examples-html
	mkdocs build
	$(MAKE) docs-copy-notebooks


serve-docs:  ## Serve docs
	mkdocs serve


docs-examples-html:  ## Run nbconvert on the docs examples
	cd $(CURDIR)/examples; jupyter nbconvert *.ipynb --output-dir=$(CURDIR)/docs/examples/ --to illusionist


docs-copy-notebooks:  ## Execute example notebooks into docs output
	cd $(CURDIR)/examples; jupyter nbconvert *.ipynb --output-dir=$(CURDIR)/site/examples/notebooks --to illusionist-nb  --execute


example:  ## Run nbconvert on one example
	cd $(CURDIR)/examples; ILLUSIONIST_DEV_MODE=0 jupyter nbconvert widget-gallery.ipynb --to illusionist


serve-examples:  ## Serve examples
	cd $(CURDIR)/examples; python -m http.server


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

