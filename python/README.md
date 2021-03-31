# illusionist

[![pypi](https://badge.fury.io/py/illusionist.svg)](https://pypi.org/project/illusionist/)
[![build](https://github.com/danielfrg/illusionist/workflows/test/badge.svg)](https://github.com/danielfrg/illusionist/actions/workflows/test.yml)
[![docs](https://github.com/danielfrg/illusionist/workflows/docs/badge.svg)](https://github.com/danielfrg/illusionist/actions/workflows/docs.yml)
[![coverage](https://codecov.io/gh/danielfrg/illusionist/branch/master/graph/badge.svg)](https://codecov.io/gh/danielfrg/illusionist?branch=master)
[![license](https://img.shields.io/:license-Apache%202-blue.svg)](https://github.com/danielfrg/illusionist/blob/master/LICENSE.txt)

Illusionist takes a Jupyter Notebook with widgets and converts it to a
an HTML report that maintains the interactivity of the widgets without a
running Jupyter kernel.

It does this by making all computation upfront and serializing all the possible outputs.
It generates a self-contained asset that you can easily drop into a file server
and have an interactive report that scales.

The main idea of Jupyter Notebooks and Jupyter widgets is to make data closer
to the code and data scientists while maintaining interactivity, they do a great job at that.
Illusionist maintains the same development workflow Jupyter users are used to by using
standard Jupyter tooling such as `ipywidgets` and `nbconvert`.
No need to import anything in your notebook to generate an interactive report using illusionist,
just run one `nbconvert` command.

The generated assets are easy to deploy, scale and have a big longevity by
removing a lot of deployment requirements and dependencies.

Learn more and see examples in [the docs](https://illusionist.danielfrg.com/).
