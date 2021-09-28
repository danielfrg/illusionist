import os
import os.path

import jinja2
from nbconvert.exporters.html import HTMLExporter

from illusionist.config import settings
from illusionist.preprocessor import IllusionistPreprocessor


@jinja2.utils.pass_context
def include_external_file(ctx, name):
    """Include an encoded base64 image"""
    with open(os.path.abspath(name), "r") as f:
        content = f.read()
    return jinja2.utils.Markup(content)


class IllusionistHTMLExporter(HTMLExporter):
    # Name for the UI menu item under "File -> Download as"
    export_from_notebook = "Illusionist HTML"
    preprocessors = [IllusionistPreprocessor]
    template_file = "illusionist/index.html.j2"
    extra_template_paths = [settings.templates_dir]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.environment.globals["dev_mode"] = settings.dev_mode

    def _init_resources(self, resources):
        resources = super()._init_resources(resources)
        resources["include_external_file"] = include_external_file
        return resources

    # Keeping this just in case
    # def default_filters(self):
    #     for pair in super().default_filters():
    #         yield pair
    #     yield ("echo_filter", self.echo_filter)

    # def echo_filter(self, text):
    #     return "echo_filter: " + text
