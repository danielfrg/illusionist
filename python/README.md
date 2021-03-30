# illusionist

[![PyPI](https://badge.fury.io/py/illusionist.svg)](https://pypi.org/project/illusionist/)
[![Testing](https://github.com/danielfrg/illusionist/workflows/test/badge.svg)](https://github.com/danielfrg/illusionist/actions)
[![License](http://img.shields.io/:license-Apache%202-blue.svg)](https://github.com/danielfrg/illusionist/blob/master/LICENSE.txt)
[![Docs](https://github.com/danielfrg/jupyter-flex/workflows/docs/badge.svg)](https://jupyter-flex.danielfrg.com/)

Illusionist takes a Jupyter Notebooks with widgets and converts it to a
dynamic HTML report that maintains the interactivity of the widgets without a
running Jupyter kernel.

It does this by making all computation upfront and serializing all the possible outputs.
It generates a self-contained asset that you can easily drop into any webserver
and have an interactive report that scales.

The main idea of Jupyter Notebooks and Jupyter widgets is to make data closer
to the data scientists while maintaining interactivity, they do a great job at that.
Illusionist maintains the same workflow Jupyter users are used to by using
regular `ipywidgets` and Jupyter tooling.
No need to import anything in your notebook, to generate a report
just run one `nbconvert` command to generate your report.

These reports are a lot easier to deploy, scale and increases their longevity by
removing a lot of the deployment requirements.

Right now it only supports the creation of one single fat HTML file which works
with small-medium reports which are the most common ones. But I have
plans to make this easier to scale to larger reports with more outputs.
