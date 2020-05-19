import os
import os.path

import jinja2
from traitlets import default, List
from nbconvert.exporters.html import HTMLExporter
from illusionist.preprocessor import IllusionistPreprocessor


@jinja2.contextfunction
def include_template(ctx, name):
    """Include a file relative to this python file
    """
    env = ctx.environment
    return jinja2.Markup(env.loader.get_source(env, name)[0])


@jinja2.contextfunction
def include_external_file(ctx, name):
    """Include an encoded base64 image
    """
    with open(os.path.abspath(name), "r") as f:
        content = f.read()
    return jinja2.Markup(content)


@jinja2.contextfunction
def include_external_base64_img(ctx, name):
    """Include an encoded base64 external image
    """
    import base64

    with open(os.path.abspath(name), "rb") as f:
        encoded_string = base64.b64encode(f.read())
    return jinja2.Markup(encoded_string.decode())


class IllusionistExporter(HTMLExporter):
    # Name for the "File -> Download as" menu in the notebook
    export_from_notebook = "Illusionist"

    extra_loaders = [jinja2.PackageLoader(__name__, "")]

    preprocessors = [IllusionistPreprocessor]

    # @default("template_file")
    # def _template_file_default(self):
    #     if self.template_extension:
    #         return "illusionist" + self.template_extension

    @default("template_name")
    def _template_name_default(self):
        return "illusionist"

    @default("template_data_paths")
    def _template_data_paths_default(self):
        this_file_dir = os.path.abspath(os.path.dirname(__file__))
        return [os.path.join(this_file_dir, "templates")]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        globals_ = {}
        globals_["include_template"] = include_template
        globals_["include_external_file"] = include_external_file
        globals_["include_external_base64_img"] = include_external_base64_img
        self.environment.globals.update(globals_)

    # def _init_resources(self, resources):
    #     resources = super()._init_resources(resources)

    #     def resources_include_widget_state(name):
    #         env = self.environment
    #         code = """THIS IS MY COOOODE"""
    #         return jinja2.Markup(code)

    #     resources["illusionist_widget_state"] = resources_include_widget_state
    #     return resources

    def default_filters(self):
        for pair in super().default_filters():
            yield pair
        yield ("test_filter", self.test_filter)

    def test_filter(self, text):
        return "test_filter: " + text
