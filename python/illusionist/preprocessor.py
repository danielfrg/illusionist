import io
import csv
import copy
import json
import itertools

from nbconvert.preprocessors import Preprocessor

from illusionist import widgets, kernel_utils, utils
from illusionist.client import IllusionistClient
from illusionist.utils import DEV_MODE


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
    "DropdownModel",
    "RadioButtonsModel",
    "SelectModel",
    "SelectionSliderModel",
    "ToggleButtonsModel",
    "SelectionRangeSliderModel",
    "SelectMultipleModel",
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


WIDGET_ONCHANGE_MIMETYPE = "application/vnd.illusionist.widget-onchange+json"


class IllusionistPreprocessor(Preprocessor, IllusionistClient):
    """
    Execute cells in the notebook
    Then looks at the widgets and generates on-change values

    This class is mostly copied from nbconvert.preprocessors.execute
    """

    def __init__(self, **kw):
        nb = kw.get("nb")
        if nb:
            del kw["nb"]
        Preprocessor.__init__(self, nb=nb, **kw)
        IllusionistClient.__init__(self, nb, **kw)

    def preprocess(self, nb, resources=None, km=None):
        # self.log_level = "DEBUG"
        self.nb = nb
        self.km = km
        self.onchange_values = {}

        resources = resources if resources else {}
        resources["illusionist_devmode"] = DEV_MODE
        if resources["illusionist_devmode"]:
            self.log.warning(
                "Illusionist DevMode is ON. "
                "Output Notebooks and HTML will contain extra cells at the end"
            )

        try:
            self.reset_execution_trackers()
            self.execute(cleanup_kc=False)

            self.nb.metadata.widgets.update(
                {WIDGET_ONCHANGE_MIMETYPE: self.widget_onchange_state}
            )
        finally:
            # Clean up
            self._cleanup_kernel()

        return nb, resources

    def post_exec(self):
        """
        This methond it's executed as part for self.execute()
        """
        # Load helper code into the kernel
        _ = self.run_code(utils.get_source(widgets))
        _ = self.run_code(utils.get_source(kernel_utils))

        # Save Notebook and widget state before executing extra code
        # nb_cells_before = copy.deepcopy(self.nb.cells)
        widget_state_before = copy.deepcopy(self.widget_state)

        value_widgets = self.run_code_eval("get_widgets_ids(kind='value')")
        control_widgets = self.run_code_eval("get_widgets_ids(kind='control')")

        # 1. Iterate the control widgets and see which outputs it affects
        affected_by = {m_id: set() for m_id in value_widgets}

        for widget_id in control_widgets:
            init_state = copy.deepcopy(self.widget_state)
            possible_values = self.possible_values(widget_id)
            widget_affects = []

            for value in possible_values[:2]:
                self.run_code(f"set_widget_value('{widget_id}', {value})")

                new_state = self.widget_state
                diff = diff_state(init_state, new_state, my_id=widget_id)
                # print(diff)
                widget_affects.extend(diff)

            for affected in widget_affects:
                affected_by[affected] |= {widget_id}

        # 2. Iterate affected_by and add matrix (per output widget) to the matrix

        # matrices is of the form: {output_id: [[ ... matrix ... ]] }
        matrices = {}

        for output_widget_id, input_widget_ids in affected_by.items():
            if len(input_widget_ids) > 0:
                values = self.widget_matrix(output_widget_id, input_widget_ids)
                matrices[output_widget_id] = {
                    "affected_by": list(input_widget_ids),
                    "values": values,
                }

        # Save the onChange state
        onChangeState = {"version_major": 1, "version_minor": 0}
        onChangeState["all_widgets"] = value_widgets
        onChangeState["control_widgets"] = control_widgets
        onChangeState["onchange"] = matrices
        self.widget_onchange_state = onChangeState

        # Set the original widget_state values back
        self.widget_state = widget_state_before

    def widget_matrix(self, output_widget_id, input_widget_ids):
        output_state = self.widget_state[output_widget_id]
        input_states = [self.widget_state[w_id] for w_id in input_widget_ids]

        # Get the product of all possible input values
        product = widget_product(input_states)

        # 2. Now we iterate the combinations of possible values
        # To create the matrix

        matrix = {}
        outputs = []
        input_ids = list()
        for inputs_set in product:

            # Update values of input widgets
            for widget_id, value in zip(input_widget_ids, inputs_set):
                self.run_code(f"set_widget_value('{widget_id}', {value})")

            # Save the new value of the output widget
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
        widget_states = []
        # print(self.widget_state)
        for widget_id in widget_ids:
            w_state = self.widget_state[widget_id]
            widget_states.append(w_state)

        return hash_fn(widget_states)

    def possible_values(self, widget_id):
        """
        Returns a list with the possible values for a widget
        """
        widget_state = self.widget_state[widget_id]
        return possible_values(widget_state)


def widget_product(input_states):
    # Make a product of all the possible widget values
    # For each input_widgets, get all possible values they can have
    possible_values_by_widget = []
    for w_state in input_states:
        values = possible_values(w_state)
        possible_values_by_widget.append(values)

    return list(itertools.product(*possible_values_by_widget))


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


def possible_values(widget_state):
    model_name = widget_state["_model_name"]
    if model_name == "IntRangeSliderModel":
        # Return all combinations that are possible: low < high
        range_ = range(
            widget_state["min"],
            widget_state["max"] + widget_state["step"],
            widget_state["step"],
        )
        ret = itertools.product(range_, range_)
        ret = [[i, j] for i, j in ret if i <= j]
        return ret
    elif model_name in NUMERIC_CONTROL_WIDGETS:
        return list(
            range(
                widget_state["min"],
                widget_state["max"] + widget_state["step"],
                widget_state["step"],
            )
        )
    elif model_name in BOOLEAN_CONTROL_WIDGETS:
        return [True, False]
    elif model_name == "SelectionRangeSliderModel":
        range_ = range(0, len(widget_state["_options_labels"]))
        ret = itertools.product(range_, range_)
        ret = [[i, j] for i, j in ret if i <= j]
        return ret
    elif model_name == "SelectMultipleModel":
        range_ = range(0, len(widget_state["_options_labels"]))
        return list(powerset(range_))
    elif model_name in SELECTION_CONTROL_WIDGETS:
        range_ = range(0, len(widget_state["_options_labels"]))
        return list(range_)
    else:
        raise Exception(f"Widget type '{model_name}' not supported.")


def powerset(iterable):
    """
    Example: powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    """
    s = list(iterable)
    return itertools.chain.from_iterable(
        itertools.combinations(s, r) for r in range(len(s) + 1)
    )


def hash_fn(w_states):
    values = []
    for w_state in w_states:
        model_name = w_state["_model_name"]

        if model_name in NUMERIC_CONTROL_WIDGETS:
            value = w_state["value"]
        elif model_name in BOOLEAN_CONTROL_WIDGETS:
            value = w_state["value"]
        elif model_name in SELECTION_CONTROL_WIDGETS:
            value = w_state["index"]
        else:
            raise Exception(f"Cannot use '{model_name}' as input")

        if isinstance(value, str):
            value = json.dumps(value)
        elif isinstance(value, bool):
            value = json.dumps(value)
        elif isinstance(value, (tuple, list)):
            value = list(value)
            value = json.dumps(value, separators=(",", ":"))
        values.append(value)

    return dumps(values)


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
