# Illusionist

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

Right now it only supports the creation of one single fat HTML file which works
with small-medium reports which are the most common ones. But I have
plans to make this easier to scale to larger reports with more outputs.

## Examples

- [A simple operation: multiplication](/examples/multiplier.html)
- [Linked widgets](/examples/linked.html)
- [Widget gallery](/examples/widget-gallery.html)
- [Matplotlib output](/examples/matplotlib.html)

## How it compares to Voila / Dash / Shiny

TODO
