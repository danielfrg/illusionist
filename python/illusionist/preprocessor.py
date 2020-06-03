import io
import csv
import copy
import json
import asyncio
import itertools

from illusionist import utils
from illusionist.utils import DEV_MODE
from illusionist import kernel_utils
from illusionist.client import IllusionistClient

from nbconvert.preprocessors import Preprocessor


NUMERIC_CONTROL_WIDGETS = (
    "IntSliderModel",
    # "FloatSlider",  # floats suck
    # "FloatLogSlider",  # floats suck
    "IntRangeSliderModel",
    # "FloatRangeSlider",  # floats suck
    "BoundedIntTextModel",
    # "BoundedFloatText",  # floats suck
    # "IntText",  # No open ended
    # "FloatText",  # No open ended
)
NUMERIC_OUTPUT_WIDGETS = NUMERIC_CONTROL_WIDGETS + (
    "IntProgressModel",
    "FloatProgressModel",
)

BOOLEAN_CONTROL_WIDGETS = ("ToggleButtonModel", "CheckboxModel")
BOOLEAN_OUTPUT_WIDGETS = BOOLEAN_CONTROL_WIDGETS + ("ValidModel",)

SELECTION_CONTROL_WIDGETS = (
    "ModelDropdownModel",
    "ModelRadioButtonsModel",
    "ModelSelectModel",
    "ModelSelectionSliderModel",
    "ModelToggleButtonsModel",
    "ModelSelectionRangeSliderModel",
    "ModelSelectMultipleModel",
)
SELECTION_OUTPUT_WIDGETS = SELECTION_CONTROL_WIDGETS

STRING_CONTROL_WIDGETS = (
    # "Text",  # No open ended
    # "Textarea",  # No opeen ended
)
STRING_OUTPUT_WIDGETS = (
    "LabelModel",
    # "HTMLModel",  # TODO
    # "HTMLMathModel",  # TODO
    # "ImageModel",  # TODO
)

OTHER_CONTROL_WIDGETS = (
    # "ButtonModel",  # TODO
    # "PlayModel",  # TODO
    # "DatePickerModel",  # TODO
    # "ColorPickerModel"  # TODO
)

CONTROL_WIDGETS = (
    NUMERIC_CONTROL_WIDGETS
    + BOOLEAN_CONTROL_WIDGETS
    + SELECTION_CONTROL_WIDGETS
    + STRING_CONTROL_WIDGETS
    + OTHER_CONTROL_WIDGETS
)

OUTPUT_WIDGETS = (
    NUMERIC_OUTPUT_WIDGETS
    + BOOLEAN_OUTPUT_WIDGETS
    + SELECTION_OUTPUT_WIDGETS
    + STRING_OUTPUT_WIDGETS
    + ("OutputModel",)
)

VALUE_WIDGETS = CONTROL_WIDGETS + OUTPUT_WIDGETS


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

    def post_exec(self):
        """
        This gets executed as part for self.execute()
        """
        # print("exec_after_notebook", self.kc)
        # Source helper code to the kernel
        _ = self.run_code(utils.get_source(kernel_utils))

        # _ = self.run_code("print(out.outputs)")
        # print(_)
        # _ = self.run_code("f.value = 1")
        # _ = self.run_code("f.value = 1\nout.get_state()")
        # print(_)
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

        # output = self.run_code("print(onchange_values)")
        # jsont_str = output.outputs[0].text
        # self.onchange_values = json.loads(jsont_str)
        # print(self.onchange_values)

        value_widgets = self.run_code_eval("get_widgets_ids(kind='value')")
        control_widgets = self.run_code_eval("get_widgets_ids(kind='control')")

        # print(self.widget_state)
        # print(control_widgets)

        # 1. Iterate the control widgets and see which outputs it affects
        affected_by = {m_id: set() for m_id in value_widgets}

        for widget_id in control_widgets:
            init_state = copy.deepcopy(self.widget_state)
            possible_values = self.run_code_eval(f"possible_values('{widget_id}')")
            widget_affects = []

            for value in possible_values[:2]:
                self.run_code(f"set_widget_value('{widget_id}', {value})")

                new_state = self.widget_state
                diff = diff_state(init_state, new_state, my_id=widget_id)
                # print(diff)
                widget_affects.extend(diff)

            for affected in widget_affects:
                affected_by[affected] |= {widget_id}

        # print(affected_by)

        # 2. Iterate affected_by and add matrix (per output widget) to the matrix

        # matrices = {output_id: [[ ... matrix ... ]] }
        matrices = {}

        for output_widget_id, input_widget_ids in affected_by.items():
            # output_widget = all_widgets[output_widget_id]
            if len(input_widget_ids) > 0:
                # input_widgets = {m_id: all_widgets[m_id] for m_id in input_widget_ids}
                # input_ids = list(input_widgets.keys())
                # return input_widgets
                # values = self.run_code_eval(
                #     f"widgets_matrix('{output_widget_id}', '{input_widget_ids}'))"
                # )
                values = self.widgets_matrix(output_widget_id, input_widget_ids)
                matrices[output_widget_id] = {
                    "affected_by": list(input_widget_ids),
                    "values": values,
                }

        ret = {"version_major": 1, "version_minor": 0}
        ret["all_widgets"] = value_widgets
        ret["control_widgets"] = control_widgets
        ret["onchange"] = matrices
        self.onchange_values = ret

        # print(ret)
        # return json.dumps(ret)

    def widgets_matrix(self, output_widget_id, input_widget_ids):
        # all_widgets = Widget.widgets
        # output_widget = all_widgets[output_widget_id]
        # input_widgets = {m_id: all_widgets[m_id] for m_id in input_widget_ids}

        # 1. Make a product of all the possible widget values

        # For each input_widgets, get all possible values they can have
        possible_values_by_widget = {}
        for widget_id in input_widget_ids:
            possible_values = self.run_code_eval(f"possible_values('{widget_id}')")
            possible_values_by_widget[widget_id] = possible_values

        list_ = possible_values_by_widget.values()
        # Prodcut is a list of lists, each item is a combination of possible
        # input widget values

        product = itertools.product(*list_)
        # print(list(product))

        # 2. Now we iterate the combinations of possible values
        # To create the matrix

        matrix = {}
        outputs = []
        input_ids = list()
        for inputs_set in product:

            # Update values of input widgets
            for i, (widget_id, value) in enumerate(zip(input_widget_ids, inputs_set)):
                self.run_code(f"set_widget_value('{widget_id}', {value})")

            # Save the new value of the output widget
            # print(hash_fn(input_widgets))
            hash_ = self.hash_fn(input_widget_ids)
            matrix[hash_] = self.get_output_value(output_widget_id)

        return matrix

    def get_output_value(self, output_widget_id):
        widget_state = self.widget_state[output_widget_id]
        model_name = widget_state["_model_name"]

        if model_name in NUMERIC_OUTPUT_WIDGETS:
            return widget_state["value"]
        elif model_name in BOOLEAN_OUTPUT_WIDGETS:
            return widget_state["value"]
        elif model_name in SELECTION_OUTPUT_WIDGETS:
            if isinstance(widget_state["index"], tuple):
                return list(widget_state["index"])
            return widget_state["index"]
        elif model_name in STRING_OUTPUT_WIDGETS:
            return widget_state["value"]
        elif model_name == "OutputModel":
            return widget_state["outputs"]
        else:

            raise Exception(f"Output Widget type '{model_name}' not supported.")

    def hash_fn(self, widget_ids):
        values = []
        # print(self.widget_state)
        for widget_id in widget_ids:
            widget_state = self.widget_state[widget_id]
            model_name = widget_state["_model_name"]

            if model_name in NUMERIC_CONTROL_WIDGETS:
                value = widget_state["value"]
            elif model_name in BOOLEAN_CONTROL_WIDGETS:
                value = widget_state["value"]
            elif model_name in SELECTION_CONTROL_WIDGETS:
                value = widget_state["index"]
            else:
                raise Exception(f"Cannot use 'f{model_name}' as input")

            if isinstance(value, str):
                value = json.dumps(value)
            elif isinstance(value, bool):
                value = json.dumps(value)
            elif isinstance(value, tuple):
                value = list(value)
                value = json.dumps(value, separators=(",", ":"))
            values.append(value)

        return dumps(values)


def diff_state(initial, new, my_id=None):
    """
    Return a list of widget model_ids that have changed based on the two widget states
    """
    diff = []
    for (init_id, init_state), (new_id, new_state) in zip(initial.items(), new.items()):
        assert init_id == new_id
        if init_state != new_state:
            diff.append(init_id)

    if my_id and my_id in diff:
        diff.remove(my_id)
    return diff


def dumps(values):
    """
    CSV Serialization
    """
    output = io.StringIO()
    writer = csv.writer(
        output,
        skipinitialspace=True,
        delimiter=",",
        quotechar='"',
        quoting=csv.QUOTE_NONNUMERIC,
    )
    writer.writerow(values)
    contents = output.getvalue()
    output.close()
    return contents.strip()


if __name__ == "__main__":
    from nbconvert.nbconvertapp import main

    main()
