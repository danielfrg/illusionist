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
        # resources["illusionist_devmode"] = False

        try:
            self.reset_execution_trackers()
            self.execute(cleanup_kc=False)

            # Source helper code to the kernel
            _ = self.run_cmd(get_source(kernel_utils))

            # _ = self.run_cmd(f"get_widgets(kind='value')", ret_output=True)
            # print(_)
            # print()

            # w_state = self.nb.metadata.widgets["application/vnd.jupyter.widget-state+json"]["state"]
            _ = self.run_cmd("onchange_values = generate_onchange()")
            output = self.run_cmd("print(onchange_values)", ret_output=True)
            # print(output)
            onchange_values = json.loads(output)

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
