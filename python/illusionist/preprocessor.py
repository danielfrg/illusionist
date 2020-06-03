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
        self.onchange_values = {}

        resources = resources if resources else {}
        resources["illusionist_devmode"] = DEV_MODE

        try:
            self.reset_execution_trackers()
            self.execute(cleanup_kc=False)

            self.set_widgets_onchange_metadata(self.onchange_values)
        finally:
            # Clean up
            self._cleanup_kernel()

        # self.resources = resources
        # print(resources)
        return nb, resources

    def exec_after_notebook(self):
        print("??????????")
        # Source helper code to the kernel
        # _ = self.run_code(get_source(kernel_utils))

        # _ = self.run_code("print(out.outputs)")
        # print(_)
        # _ = self.run_code("f.value = 1")
        _ = self.run_code("f.value = 1\nout.get_state()")
        # _ = self.run_code("out.get_state()")
        # print(_)
        # print(self.widget_state)
        # _ = self.run_code("print(out.outputs)")

        # print(self.run_code("f.value"))
        # _ = self.run_cmd(f"f.value = 1")
        # _ = self.run_cmd(f"print(f.value)", ret_output=True)
        # print(_)
        # _ = self.run_cmd(f"out", ret_output=True)
        # print(_)

        ####

        # _ = self.run_code("onchange_values = generate_onchange()")
        # print(_)
        # output = self.run_code("print(onchange_values)")
        # jsont_str = output.outputs[0].text
        # self.onchange_values = json.loads(jsont_str)
        # print(self.onchange_values)


def get_source(code):
    import inspect

    return inspect.getsource(code)
