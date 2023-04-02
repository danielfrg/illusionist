# illusionist

[![pypi](https://img.shields.io/pypi/v/illusionist.svg)](https://pypi.org/project/illusionist/)
[![build](https://github.com/danielfrg/illusionist/workflows/test/badge.svg)](https://github.com/danielfrg/illusionist/actions/workflows/test.yml)
[![docs](https://github.com/danielfrg/illusionist/workflows/docs/badge.svg)](https://github.com/danielfrg/illusionist/actions/workflows/docs.yml)
[![coverage](https://codecov.io/gh/danielfrg/illusionist/branch/master/graph/badge.svg)](https://codecov.io/gh/danielfrg/illusionist?branch=master)
[![license](https://img.shields.io/:license-Apache%202-blue.svg)](https://github.com/danielfrg/illusionist/blob/master/LICENSE.txt)

Illusionist takes a Jupyter Notebook with a kernel and widgets and exports a
static HTML report that maintains the interactivity of the widgets without a
live Jupyter kernel.

It does this by pre-calculating and serializing all the possible outputs
and it generates a self-contained asset that has no runtime requirements.

A good analogy is the [static HTML export](https://nextjs.org/docs/advanced-features/static-html-export)
of a dynamic web server like [Next.JS](https://nextjs.org/).
A Jupyter Notebook connected to a live kernel is equivalent to a web server and
an illusionist report would be the static HTML version of the content.
An static site generator pre-renders the content and illusionist pre-calculates
the outputs of the widgets.

The main idea of Jupyter Notebooks and Jupyter widgets is to make data closer
to the code and data scientists while maintaining interactivity, they do a great job at that.
Illusionist maintains the same development workflow Jupyter users are used to by using
standard Jupyter tooling such as `ipywidgets` and `nbconvert`.
No need to import anything in your notebook to generate an interactive report using illusionist,
just run one `nbconvert` command.

The generated assets are easy to deploy, scale and have a big longevity by
removing a lot of deployment requirements and dependencies.
Like a regular [static web page](https://en.wikipedia.org/wiki/Static_web_page).

Learn more and see examples at [illusionist.danielfrg.com](https://illusionist.danielfrg.com).
