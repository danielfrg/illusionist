import copy
import csv
import io
import itertools
import json
import logging

import structlog
from nbconvert.preprocessors import Preprocessor

import illusionist.widgets_str as W
from illusionist import kernel_utils, utils, widgets
from illusionist.client import IllusionistClient
from illusionist.config import settings

log = structlog.get_logger()

structlog.configure(
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
)


WIDGET_ONCHANGE_MIMETYPE = "application/vnd.illusionist.widget-onchange+json"


class IllusionistPreprocessor(Preprocessor, IllusionistClient):
    """
    Executes the notebook and then looks at the widgets available and generates
    a new `onchange` state that is saved into the HTML output.

    This `onchange` state contains all possible values for a widget
    based on the control widget it is affected by.

    ```
    {
        "version_major": 1, "version_minor": 0,
        "all_widgets": [ value_widgets ],
        "control_widgets": [ control_widgets ],
        "onchange": {
            <value_widget_id>: {
                "affected_by": [ control_widget_ids ],
                "values": [ [ ... ] ]
            }
        }
    }
    ```

    This class is based and adapted from nbconvert.preprocessors.execute:
    https://github.com/jupyter/nbconvert/blob/main/nbconvert/preprocessors/execute.py
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
        resources["illusionist_devmode"] = settings.dev_mode
        if resources["illusionist_devmode"]:
            self.log.warning(
                "Illusionist Dev Mode is ON. "
                "Output HTML or Notebook will contain extra cells at the end"
            )

        try:
            self.reset_execution_trackers()
            self.execute(cleanup_kc=False)

            # self.widget_onchange_state is created on self.after_notebook
            self.nb.metadata.widgets.update(
                {WIDGET_ONCHANGE_MIMETYPE: self.widget_onchange_state}
            )
        finally:
            # Clean up
            self._cleanup_kernel()

        return nb, resources

    def after_notebook(self):
        """
        Overwrites IllusionistClient

        This is called after the regular notebook cells have been executed

        It iterates all the widgets and generate static properties

        Like Next.JS `getStaticPaths`:
        https://nextjs.org/docs/basic-features/data-fetching#getstaticpaths-static-generation
        """
        # Load helper code into the kernel
        _ = self.exec_code(utils.get_source(widgets))
        _ = self.exec_code(utils.get_source(kernel_utils))

        # Save original Notebook and widget state
        # nb_cells_before = copy.deepcopy(self.nb.cells)
        base_widget_state = copy.deepcopy(self.widget_state)

        value_widgets, control_widgets = self.get_target_widgets()

        # 1. Get a list of how value widgets are affected by control widgets
        affected_by = self.get_affected_widgets(control_widgets, value_widgets)
        # log.msg("Affected by dict", value=affected_by)

        # 2. Iterate affected_by and add matrix (per output widget) to the matrix
        static_values = self.get_static_values(affected_by)
        # log.msg("Static values dict", value=static_values)

        # Save the onchange state
        onChangeState = {"version_major": 1, "version_minor": 0}
        onChangeState["all_widgets"] = value_widgets
        onChangeState["control_widgets"] = control_widgets
        onChangeState["onchange"] = static_values
        self.widget_onchange_state = onChangeState

        # Set the original widget_state back to the original ones
        self.widget_state = base_widget_state

    def get_target_widgets(self):
        value_widgets = self.exec_code("get_widgets_ids(kind='value')")
        value_widgets = self.eval_cell(value_widgets)

        for w in value_widgets:
            name = self.widget_state[w]["_model_name"]
            # log.msg("Value Widget", id=w, model=name)

        control_widgets = self.exec_code("get_widgets_ids(kind='control')")
        control_widgets = self.eval_cell(control_widgets)

        for w in control_widgets:
            name = self.widget_state[w]["_model_name"]
            # log.msg("Control Widget", id=w, model=name)

        return value_widgets, control_widgets

    def get_affected_widgets(self, control_widgets, value_widgets):
        """
        Iterates the control widgets and see which value widgets are affected
        by changes to each of them.

        Returns
        -------
            dictionary of `{value_w_id: <set of control_w_ids that produce a change>}
        """
        affected_by = {m_id: set() for m_id in value_widgets}

        for widget_id in control_widgets:
            init_state = copy.deepcopy(self.widget_state)
            possible_values = self.possible_values(widget_id)
            widget_affects = []

            # Iterate all possible values of the control widget
            # and record if any widget state changed
            for value in possible_values:
                self.exec_code(f"set_widget_value('{widget_id}', {value})")
                new_state = self.widget_state
                diff = diff_state(init_state, new_state, my_id=widget_id)
                widget_affects.extend(diff)

            # For the affected widgets save them
            for affected in widget_affects:
                # The or operation of set will add them to the list
                affected_by[affected] |= {widget_id}

        return affected_by

    def get_static_values(self, affected_by):
        """
        For the list of widgets and its affected links

        Iterate affected_by and create a matrix (per output widget)
        Returns
        -------
            dictionary: { value_widget_id: {
                "affected_by": [control_widget_ids],
                "values": [ ... ]
            }}
        """
        static_values = {}

        for value_w_id, control_w_ids in affected_by.items():
            if len(control_w_ids) > 0:
                values = self.get_static_values_by_widget(
                    value_w_id, control_w_ids
                )
                static_values[value_w_id] = {
                    "affected_by": list(control_w_ids),
                    "values": values,
                }
        return static_values

    def get_static_values_by_widget(self, value_w_id, control_w_ids):
        """
        For a value widget return a matrix of:
        ```
            { hash(control_widget_values): <value_widget value>}
        ```
        Returns
        -------
            dictionary
        """
        # 1. Get all possible combinations control widget values that affect
        # this value widget
        control_w_states = [self.widget_state[w_id] for w_id in control_w_ids]
        product = widget_values_product(control_w_states)

        # 2. Iterate the combinations of possible values to create a matrix
        matrix = {}
        for controls_set in product:
            # Update values of control widgets
            for widget_id, value in zip(control_w_ids, controls_set):
                self.exec_code(f"set_widget_value('{widget_id}', {value})")

            # Save the new value of the output widget
            hash_ = self.hash_fn(control_w_ids)
            matrix[hash_] = self.get_widget_value(value_w_id)

        return matrix

    def get_widget_value(self, widget_id):
        """
        Based on the widget model return the current value for a widget id
        This value is the one we serialize on the onChangeState
        """
        widget_state = self.widget_state[widget_id]
        model_name = widget_state["_model_name"]

        if model_name in W.NUMERIC_OUTPUT_WIDGETS:
            return widget_state["value"]
        elif model_name in W.BOOLEAN_OUTPUT_WIDGETS:
            return widget_state["value"]
        elif model_name in W.SELECTION_OUTPUT_WIDGETS:
            if isinstance(widget_state["index"], tuple):
                return list(widget_state["index"])
            return widget_state["index"]
        elif model_name in W.STRING_OUTPUT_WIDGETS:
            return widget_state["value"]
        elif model_name == "OutputModel":
            return widget_state["outputs"]
        else:
            raise Exception(
                f"Output Widget type '{model_name}' not supported."
            )

    def hash_fn(self, widget_ids):
        """Calculate a hash"""
        widget_states = []
        for widget_id in widget_ids:
            w_state = self.widget_state[widget_id]
            widget_states.append(w_state)

        return hash_fn_plain(widget_states)

    def possible_values(self, widget_id):
        """Return a list of all the possible values for a widget"""
        widget_state = self.widget_state[widget_id]
        return possible_values(widget_state)


def widget_values_product(widget_states):
    """
    Make a product of all the possible widget values
    For each control_widget, get all possible values they can have

    The product is helpful when there are more than 1 control widget
    that change one value widget
    """
    all_possible_values = []
    for w_state in widget_states:
        values = possible_values(w_state)
        all_possible_values.append(values)

    return list(itertools.product(*all_possible_values))


def diff_state(initial, new, my_id=None):
    """
    Return a list of widget model_ids that have changed based on two widget
    states
    """
    diff = []
    for (init_id, init_state), (new_id, new_state) in zip(
        initial.items(), new.items()
    ):
        assert init_id == new_id
        if init_state != new_state:
            diff.append(init_id)

    if my_id and my_id in diff:
        diff.remove(my_id)
    return diff


def possible_values(widget_state):
    """
    Return a list of all the possible values for a single widget
    """
    model_name = widget_state["_model_name"]
    if model_name == "IntRangeSliderModel":
        range_ = range(
            widget_state["min"],
            widget_state["max"] + widget_state["step"],
            widget_state["step"],
        )
        ret = itertools.product(range_, range_)
        ret = [[i, j] for i, j in ret if i <= j]
        return ret
    elif model_name in W.NUMERIC_CONTROL_WIDGETS:
        return list(
            range(
                widget_state["min"],
                widget_state["max"] + widget_state["step"],
                widget_state["step"],
            )
        )
    elif model_name in W.BOOLEAN_CONTROL_WIDGETS:
        return [True, False]
    elif model_name == "SelectionRangeSliderModel":
        range_ = range(0, len(widget_state["_options_labels"]))
        ret = itertools.product(range_, range_)
        ret = [[i, j] for i, j in ret if i <= j]
        return ret
    elif model_name == "SelectMultipleModel":
        range_ = range(0, len(widget_state["_options_labels"]))
        return list(powerset(range_))
    elif model_name in W.SELECTION_CONTROL_WIDGETS:
        range_ = range(0, len(widget_state["_options_labels"]))
        return list(range_)
    else:
        raise Exception(f"Widget type '{model_name}' not supported.")


def powerset(iterable):
    """
    Example
    -------
        powerset([1, 2, 3]) -> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    """
    s = list(iterable)
    return itertools.chain.from_iterable(
        itertools.combinations(s, r) for r in range(len(s) + 1)
    )


def hash_fn_plain(widget_states):
    """
    Hash all the possible values of a group of widgets.
    """
    values = []
    for w_state in widget_states:
        model_name = w_state["_model_name"]

        if model_name in W.NUMERIC_CONTROL_WIDGETS:
            value = w_state["value"]
        elif model_name in W.BOOLEAN_CONTROL_WIDGETS:
            value = w_state["value"]
        elif model_name in W.SELECTION_CONTROL_WIDGETS:
            value = w_state["index"]
        else:
            raise Exception(f"Cannot use '{model_name}' as input")

        if isinstance(value, str):
            value = json.dumps(value)
        elif isinstance(value, bool):
            value = json.dumps(value)
        elif isinstance(value, (tuple, list)):
            value = list(value)
            # separators are the same but without the spaces
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
