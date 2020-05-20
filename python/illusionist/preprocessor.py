import asyncio
import json

from illusionist.utils import DEV_MODE
from illusionist import kernel_utils
from illusionist.client import IllusionistClient

from nbconvert.preprocessors import Preprocessor


class IllusionistPreprocessor(Preprocessor, IllusionistClient):
    """
    Execute cells in the notebook
    Then looks at the widgets and generates on-change values

    This class is mostly copied from nbconvert.preprocessors.execute
    """

    def __init__(self, **kw):
        nb = kw.get("nb")
        Preprocessor.__init__(self, nb=nb, **kw)
        IllusionistClient.__init__(self, nb, **kw)

    def preprocess(self, nb, resources=None, km=None):
        # self.log_level = "DEBUG"
        self.nb = nb
        self.km = km

        resources = resources if resources else {}
        resources["illusionist_devmode"] = DEV_MODE
        resources["illusionist_devmode"] = False

        try:
            self.reset_execution_trackers()
            self.execute(cleanup_kc=False)

            # Source helper code
            _ = self.run_cmd(get_source(kernel_utils))

            _ = self.run_cmd("widget_vars = generate_json()")
            output_json = self.run_cmd("print(widget_vars)", ret_output=True)
            onchange_values = json.loads(output_json)
            # print(onchange_values)

            # print(self.widget_state)
            self.set_widgets_onchange_metadata(onchange_values)
        finally:
            # Clean up
            self._cleanup_kernel()

        # self.resources = resources
        # print(resources)
        return nb, resources


def get_source(code):
    import inspect

    return inspect.getsource(code)
