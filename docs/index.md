# Illusionist

Status: experimentation

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

## Installation

```
pip install illusionist
```

## Usage

To generate an HTML report:

```
jupyter nbconvert --to illusionist your-notebook.ipynb
```

To add execute the Notebook and add the widget the metadata to an `.ipynb` file:

```
jupyter nbconvert --to illusionist-nb --execute your-notebook.ipynb --output=output-notebook.ipynb
```

[Learn more](/usage).

## Examples

- Widget Galley: [html](/examples/widget-gallery.html) - [ipynb](https://nbviewer.danielfrg.com/nb/raw.githubusercontent.com/danielfrg/illusionist/master/examples/widget-gallery.ipynb) - [dashboard](https://jupyter-flex.netlify.app/examples/illusionist/widget-gallery.html)
- Output Widgets using Matplotlib: [html](/examples/matplotlib.html) - [ipynb](https://nbviewer.danielfrg.com/nb/raw.githubusercontent.com/danielfrg/illusionist/master/examples/matplotlib.ipynb) - [dashboard](https://jupyter-flex.netlify.app/examples/illusionist/matplotlib.html)
- Multiplier: [html](/examples/multiplier.html) - [ipynb](https://nbviewer.danielfrg.com/nb/raw.githubusercontent.com/danielfrg/illusionist/master/examples/multiplier.ipynb)
- Linked Widgets: [html](/examples/linked.html) - [ipynb](https://nbviewer.danielfrg.com/nb/raw.githubusercontent.com/danielfrg/illusionist/master/examples/linked.ipynb) - [dashboard](https://jupyter-flex.netlify.app/examples/illusionist/linked.html)

