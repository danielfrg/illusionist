# illusionist

[![PyPI](https://badge.fury.io/py/illusionist.svg)](https://pypi.org/project/illusionist/)
[![Testing](https://github.com/danielfrg/illusionist/workflows/test/badge.svg)](https://github.com/danielfrg/illusionist/actions)
[![Docs](https://github.com/danielfrg/illusionist/workflows/docs/badge.svg)](https://illusionist.extrapolations.dev/)
[![Coverage Status](https://codecov.io/gh/danielfrg/illusionist/branch/master/graph/badge.svg)](https://codecov.io/gh/danielfrg/illusionist?branch=master)
[![License](http://img.shields.io/:license-Apache%202-blue.svg)](https://github.com/danielfrg/illusionist/blob/master/LICENSE.txt)

Status: experimentation

Illusionist takes a Jupyter Notebooks with widgets and converts it to a
dynamic HTML report that maintains the interactivity of the widgets without a
running Jupyter kernel.

It does this by making all computation upfront and serializing all the possible outputs.
It generates a self-contained asset that you can easily drop into any file server
and have an interactive report that scales.

The main idea of Jupyter Notebooks and Jupyter widgets is to make data closer
to the code and data scientists while maintaining interactivity, they do a great job at that.
Illusionist maintains the same workflow Jupyter users are used to by using
regular `ipywidgets` and Jupyter tooling.
No need to import anything in your notebook, to generate a illusionist report
just run one `nbconvert` command to generate your report.

These reports are a lot easier to deploy, scale very easily and increases their longevity by
removing a lot of deployment requirements and dependencies.

Learn more and see examples in [the docs](https://illusionist.extrapolations.dev/)
