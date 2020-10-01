import os
import sys
import os.path

import jinja2
from nbconvert.exporters.html import HTMLExporter
from traitlets import List, default

from illusionist.utils import DEV_MODE
from illusionist.preprocessor import IllusionistPreprocessor


@jinja2.contextfunction
def include_external_file(ctx, name):
    """Include an encoded base64 image"""
    with open(os.path.abspath(name), "r") as f:
        content = f.read()
    return jinja2.Markup(content)


class IllusionistHTMLExporter(HTMLExporter):
    # Name for the menu item under "File -> Download as" in the IDE
    export_from_notebook = "Illusionist HTML"
    preprocessors = [IllusionistPreprocessor]

    @default("template_name")
    def _template_name_default(self):
        return "illusionist"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.environment.globals["dev_mode"] = DEV_MODE

    def _init_resources(self, resources):
        resources = super()._init_resources(resources)

        resources["include_external_file"] = include_external_file
        return resources

    def default_filters(self):
        for pair in super().default_filters():
            yield pair
        yield ("test_filter", self.test_filter)

    def test_filter(self, text):
        return "test_filter: " + text
