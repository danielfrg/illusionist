import asyncio
import json

from illusionist import kernel_utils
from illusionist.client import IllusionistClient


from nbconvert.preprocessors import ExecutePreprocessor


def get_source(code):
    import inspect

    return inspect.getsource(code)


class IllusionistPreprocessor(ExecutePreprocessor):
    """
    Execute cells in the notebook
    Then looks at the widgets and generates on-change values
    """

    # def preprocess(self, nb, resources=None, km=None):
    #     resources = resources if resources else {}
    #     resources["illusionist_resource"] = "from preprocessor"

    #     illusionist = IllusionistClient(nb)
    #     client = illusionist
    #     # client.log_level = "DEBUG"

    #     client.execute(cleanup_kc=False)

    #     # Source helper code
    #     _ = client.run_cmd(get_source(kernel_utils))

    #     _ = client.run_cmd("widget_vars = generate_json()")
    #     output_json = client.run_cmd("print(widget_vars)", ret_output=True)
    #     onchange_values = json.loads(output_json)
    #     # print(onchange_values)

    #     # print(client.widget_state)
    #     client.set_widgets_onchange_metadata(onchange_values)

    #     # Clean up
    #     client._cleanup_kernel()

    #     self.resources = resources
    #     # print(resources)
    #     return nb, resources
