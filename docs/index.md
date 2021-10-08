# Illusionist

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

## Installation

```shell
pip install illusionist
```

## Usage

To generate an HTML report:

```shell
jupyter nbconvert --to illusionist your-notebook.ipynb
```

To add execute the Notebook and add the widget the metadata to an `.ipynb` file:

```shell
jupyter nbconvert --to illusionist-nb --execute your-notebook.ipynb --output=output-notebook.ipynb
```

[Learn more](/usage).

## Examples

- Linked Widgets: [html](/examples/linked.html) - [ipynb](https://nbviewer.danielfrg.com/notebook#raw.githubusercontent.com/danielfrg/illusionist/master/examples/linked.ipynb) - [dashboard](https://jupyter-flex.netlify.app/examples/illusionist/linked.html)
- Multiplier: [html](/examples/multiplier.html) - [ipynb](https://nbviewer.danielfrg.com/notebook#raw.githubusercontent.com/danielfrg/illusionist/master/examples/multiplier.ipynb)
- Output Widgets using Matplotlib: [html](/examples/matplotlib.html) - [ipynb](https://nbviewer.danielfrg.com/notebook#raw.githubusercontent.com/danielfrg/illusionist/master/examples/matplotlib.ipynb) - [dashboard](https://jupyter-flex.netlify.app/examples/illusionist/matplotlib.html)
- Pandas DataFrame: [html](/examples/pandas.html) - [ipynb](https://nbviewer.danielfrg.com/notebook#raw.githubusercontent.com/danielfrg/illusionist/master/examples/pandas.ipynb)
- Widget Galley: [html](/examples/widget-gallery.html) - [ipynb](https://nbviewer.danielfrg.com/notebook#raw.githubusercontent.com/danielfrg/illusionist/master/examples/widget-gallery.ipynb) - [dashboard](https://jupyter-flex.netlify.app/examples/illusionist/widget-gallery.html)

