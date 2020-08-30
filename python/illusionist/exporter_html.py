import os
import sys
import os.path

import jinja2
from nbconvert.exporters.html import HTMLExporter
from traitlets import List, default

from illusionist.preprocessor import IllusionistPreprocessor


@jinja2.contextfunction
def include_template(ctx, name):
    """Include a file relative to this python file"""
    env = ctx.environment
    return jinja2.Markup(env.loader.get_source(env, name)[0])


@jinja2.contextfunction
def include_external_file(ctx, name):
    """Include an encoded base64 image"""
    with open(os.path.abspath(name), "r") as f:
        content = f.read()
    return jinja2.Markup(content)


@jinja2.contextfunction
def include_external_base64_img(ctx, name):
    """Include an encoded base64 external image"""
    import base64

    with open(os.path.abspath(name), "rb") as f:
        encoded_string = base64.b64encode(f.read())
    return jinja2.Markup(encoded_string.decode())


class IllusionistHTMLExporter(HTMLExporter):
    # Name for the menu item under "File -> Download as" in the IDE
    export_from_notebook = "Illusionist HTML"
    preprocessors = [IllusionistPreprocessor]

    @property
    def template_path(self):
        """
        Append template intalled to share
        This is compat code until nbconvert 6.0.0 lands
        The structure of the project here is whats 6.0.0 will use
        """
        return super().template_path + [
            os.path.join(
                sys.prefix, "share", "jupyter", "nbconvert", "templates", "illusionist"
            )
        ]

    def _template_file_default(self):
        """
        We want to use the new template we ship with our library.
        """
        return "index"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        globals_ = {}
        globals_["include_template"] = include_template
        globals_["include_external_file"] = include_external_file
        globals_["include_external_base64_img"] = include_external_base64_img
        self.environment.globals.update(globals_)

    def default_filters(self):
        for pair in super().default_filters():
            yield pair
        yield ("test_filter", self.test_filter)

    def test_filter(self, text):
        return "test_filter: " + text
