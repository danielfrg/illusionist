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
No need to import anything in your notebook, to generate an Illusionist report,
just run one `nbconvert` command.

These assets are easy to deploy, scale easily and have a big longevity by
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

Voila, Dash and Shiny are great tools thats allow users to create dashboards based
on Python and R code, they are served by and connected to a running Python or R process,
this allows for birectional communication between the frontend and the backend
and results in very dynamic dashboards.

This is great if you data changes constanty, are connecting to external data
sources or APIs, or have complex logic in your dashboards.
The annoying part comes when you try to deploy any built assets because it requires
to have a running Python or R process.
There are tons of solutions out there to make this process easier but the requirements
of a handling Python/R dependencies and a running process are always there
everytime you want to update or deploy an app.

We believe most dashboard and reports do not need a live Python or R process.
Most reports only need to be updated when the underlying data is updated.
Most of those are only going to be generated once!

Some of those reports could use some interactivity based on Widgets
that make that the user experience better. Thats where illusionist comes in.

