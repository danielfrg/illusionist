SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

PWD := $(shell pwd)
PYTEST_K ?= ""


first: help

# ------------------------------------------------------------------------------
# Package build

build: npm-build python-build  ## Build assets and Python package


# ------------------------------------------------------------------------------
# Python

python-build:  ## Build Python package (sdist)
	cd $(CURDIR)/python; python setup.py sdist


env:  ## Create dev environment
	cd $(CURDIR)/python; conda env create


extensions:  ## Install Jupyter extensions
	jupyter labextension install @jupyter-widgets/jupyterlab-manager


develop:  ## Install package for development
	cd $(CURDIR)/python; python -m pip install --no-build-isolation -e . ;


check:  ## Check linting
	cd $(CURDIR)/python; flake8
	cd $(CURDIR)/python; isort --check-only --diff --recursive --project jupyter_flex --section-default THIRDPARTY .
	cd $(CURDIR)/python; black --check .


fmt:  ## Format source
	cd $(CURDIR)/python; isort --recursive --project jupyter-flex --section-default THIRDPARTY .
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
	rm -rf site docs/examples


# ------------------------------------------------------------------------------
# JS

npm-build:  ## Build JS
	cd $(CURDIR)/js/; npm run build


npm-install:  ## Install JS dependencies
	cd $(CURDIR)/js/; npm install


npm-dev:  ## Build JS with watch
	cd $(CURDIR)/js/; npm run dev


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


clean-js:  # Clean JS
	rm -rf "examples/static/*(.js|.js.map|.svg|.woff|.woff2|.eot|.ttf)"
	cd js/; rm -rf .cache dist lib


# ------------------------------------------------------------------------------
# Docs

.PHONY: examples
examples:  ## Run nbconvert the examples (dev)
	ILLUSIONIST_DEV_MODE=0 jupyter nbconvert ./examples/widget-gallery.ipynb --to illusionist
	ILLUSIONIST_DEV_MODE=0 jupyter nbconvert ./examples/multiplier.ipynb --to illusionist
	ILLUSIONIST_DEV_MODE=0 jupyter nbconvert ./examples/linked.ipynb --to illusionist
	ILLUSIONIST_DEV_MODE=0 jupyter nbconvert ./examples/matplotlib.ipynb --to illusionist
	ILLUSIONIST_DEV_MODE=0 jupyter nbconvert ./examples/widget-gallery.ipynb --output=widget-gallery.ipynb --to illusionist-nb --execute
	ILLUSIONIST_DEV_MODE=0 jupyter nbconvert ./examples/multiplier.ipynb --output=multiplier.ipynb --to illusionist-nb --execute
	ILLUSIONIST_DEV_MODE=0 jupyter nbconvert ./examples/linked.ipynb --output=linked.ipynb --to illusionist-nb --execute
	ILLUSIONIST_DEV_MODE=0 jupyter nbconvert ./examples/matplotlib.ipynb --output=matplotlib.ipynb --to illusionist-nb --execute



serve-examples:  ## Serve examples
	cd $(CURDIR)/examples; python -m http.server


docs:  docs-examples  ## Build mkdocs
	mkdocs build --config-file $(CURDIR)/mkdocs.yml


docs-examples:  ## Run nbconvert on the docs examples
	jupyter nbconvert --to illusionist ./examples/widget-gallery.ipynb --output-dir=./docs/examples/
	jupyter nbconvert --to illusionist ./examples/multiplier.ipynb --output-dir=./docs/examples/
	jupyter nbconvert --to illusionist ./examples/linked.ipynb --output-dir=./docs/examples/
	jupyter nbconvert --to illusionist ./examples/matplotlib.ipynb --output-dir=./docs/examples/


serve-docs:  ## Serve docs
	mkdocs serve


# ------------------------------------------------------------------------------
# Other

cleanall: cleanpython cleanjs  ## Clean everything
	rm -rf site
	cd $(CURDIR)/examples/; rm -rf *.html
	cd $(CURDIR)/python/; rm -rf *.egg-info
	cd $(CURDIR)/js/; rm -rf node_modules


help:  ## Show this help menu
	@grep -E '^[0-9a-zA-Z_-]+:.*?##.*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?##"; OFS="\t\t"}; {printf "\033[36m%-30s\033[0m %s\n", $$1, ($$2==""?"":$$2)}'

