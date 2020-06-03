# This code is executed on the Kernel that also executes the notebook
import json
import itertools
from ipywidgets import *  # noqa


NUMERIC_CONTROL_WIDGETS = (
    IntSlider,
    # FloatSlider,  # floats suck
    # FloatLogSlider,  # floats suck
    IntRangeSlider,
    # FloatRangeSlider,  # floats suck
    BoundedIntText,
    # BoundedFloatText,  # floats suck
    # IntText,  # No open ended
    # FloatText,  # No open ended
)
NUMERIC_OUTPUT_WIDGETS = NUMERIC_CONTROL_WIDGETS + (IntProgress, FloatProgress)

BOOLEAN_CONTROL_WIDGETS = (ToggleButton, Checkbox)
BOOLEAN_OUTPUT_WIDGETS = BOOLEAN_CONTROL_WIDGETS + (Valid,)

SELECTION_CONTROL_WIDGETS = (
    Dropdown,
    RadioButtons,
    Select,
    SelectionSlider,
    ToggleButtons,
    SelectionRangeSlider,
    SelectMultiple,
)
SELECTION_OUTPUT_WIDGETS = SELECTION_CONTROL_WIDGETS

STRING_CONTROL_WIDGETS = (
    # Text,  # No open ended
    # Textarea,  # No opeen ended
)
STRING_OUTPUT_WIDGETS = (
    Label,
    # HTML,  # TODO
    # HTMLMath,  # TODO
    # Image,  # TODO
)

OTHER_CONTROL_WIDGETS = (
    # Button,  # TODO
    # Play,  # TODO
    # DatePicker,  # TODO
    # ColorPicker  # TODO
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
    + (Output,)
)

VALUE_WIDGETS = CONTROL_WIDGETS + OUTPUT_WIDGETS
LAYOUT_WIDGETS = Box, HBox, VBox, Accordion, Tab


def powerset(iterable):
    """
    Example: powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    """
    s = list(iterable)
    return itertools.chain.from_iterable(
        itertools.combinations(s, r) for r in range(len(s) + 1)
    )


def frange(x, y, z):
    """
    Like `range` but for floats as inputs

    This is stupid and i bet its broken in a lot of ways
    From: https://stackoverflow.com/questions/7267226/range-for-floats
    """
    multiplier = 10 * (y - x) / z
    min_ = int(x * multiplier)
    max_ = int(y * multiplier)
    step_ = int(z * multiplier)
    # print(min_, max_, step_)
    return [x / multiplier for x in range(min_, max_ + step_, step_)]


def get_widgets_ids(widgets=None, kind=None):
    """
    Return all widgets that are used in the notebook
    Returns a dictionary with
        {model_id: widget_object}
    """
    # The `Widgets` class has a registry of all the widgets that were used
    all_widgets = widgets if widgets else Widget.widgets

    if kind is None:
        return list(all_widgets.keys())

    if kind == "value":
        value_widgets = []
        for model_id, obj in all_widgets.items():
            if isinstance(obj, VALUE_WIDGETS):
                value_widgets.append(model_id)
        return value_widgets

    if kind == "control":
        control_widgets = []
        for model_id, obj in all_widgets.items():
            if isinstance(obj, CONTROL_WIDGETS) and not obj.disabled:
                control_widgets.append(model_id)
        return control_widgets


def get_widgets(widgets=None, kind=None):
    """
    Return all widgets that are used in the notebook
    Returns a dictionary with
        {model_id: widget_object}
    """
    # The `Widgets` class has a registry of all the widgets that were used
    all_widgets = widgets if widgets else Widget.widgets

    if kind is None:
        return all_widgets

    if kind == "value":
        value_widgets = {}
        for model_id, obj in all_widgets.items():
            if isinstance(obj, VALUE_WIDGETS):
                value_widgets[model_id] = obj
        return value_widgets

    if kind == "control":
        control_widgets = {}
        for model_id, obj in all_widgets.items():
            if isinstance(obj, CONTROL_WIDGETS) and not obj.disabled:
                control_widgets[model_id] = obj
        return control_widgets


def get_widget_output(widget):
    """
    Get the Output value of a widget that we will serialize in the matrix
    """
    if isinstance(widget, NUMERIC_OUTPUT_WIDGETS):
        return widget.value
    elif isinstance(widget, BOOLEAN_OUTPUT_WIDGETS):
        return widget.value
    elif isinstance(widget, SELECTION_OUTPUT_WIDGETS):
        if isinstance(widget.index, tuple):
            return list(widget.index)
        return widget.index
    elif isinstance(widget, STRING_OUTPUT_WIDGETS):
        return widget.value
    elif isinstance(widget, Output):
        return widget.get_state()["outputs"]
    else:
        widget_type = type(widget)
        raise Exception(f"Output Widget type 'f{widget_type}' not supported.")


def set_widget_value(widget_id, value):
    """
    Set the value of a widget, based on a possible value
    """
    widget = Widget.widgets[widget_id]
    if isinstance(widget, NUMERIC_OUTPUT_WIDGETS):
        widget.value = value
        # raise Exception(widget, value, widget.value)
    elif isinstance(widget, BOOLEAN_OUTPUT_WIDGETS):
        widget.value = value
    elif isinstance(widget, SELECTION_OUTPUT_WIDGETS):
        widget.index = value
    elif isinstance(widget, STRING_OUTPUT_WIDGETS):
        return widget.value
    else:
        widget_type = type(widget)
        raise Exception(f"Cannot set value on widget type: 'f{widget_type}'")


def possible_values(widget_id):
    """
    Returns a list with the possible values for a widget
    """
    widget = Widget.widgets[widget_id]
    if isinstance(widget, (IntSlider, BoundedIntText)):
        return list(range(widget.min, widget.max + widget.step, widget.step))
    if isinstance(widget, (IntRangeSlider,)):
        # Return all combinations that are possible: low < high
        range_ = range(widget.min, widget.max + widget.step, widget.step)
        ret = itertools.product(range_, range_)
        ret = [[i, j] for i, j in ret if i <= j]
        return ret
    elif isinstance(widget, BOOLEAN_CONTROL_WIDGETS):
        return [True, False]
    elif isinstance(
        widget, (Dropdown, RadioButtons, Select, SelectionSlider, ToggleButtons)
    ):
        range_ = range(0, len(widget.options))
        return list(range_)
    elif isinstance(widget, SelectionRangeSlider):
        range_ = range(0, len(widget.options))
        ret = itertools.product(range_, range_)
        ret = [[i, j] for i, j in ret if i <= j]
        return ret
    elif isinstance(widget, SelectMultiple):
        range_ = range(0, len(widget.options))
        return list(powerset(range_))
    else:
        widget_type = type(widget)
        raise Exception(f"Widget type 'f{widget_type}' not supported.")


def get_state(widgets, b=False):
    """
    Get the state of all widgets
    """
    ret = {}
    for model_id, widget in widgets.items():
        if isinstance(widget, Output):
            if b:
                raise Exception(widget.outputs)
            ret[model_id] = widget.outputs
        else:
            ret[model_id] = widget.value
    return ret


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


def generate_onchange(widgets=None):
    all_widgets = get_widgets(widgets=widgets)
    value_widgets = get_widgets(widgets=widgets, kind="value")
    control_widgets = get_widgets(widgets=widgets, kind="control")

    ret = {"version_major": 1, "version_minor": 0}
    ret["all"] = [m_id for m_id, w in value_widgets.items()]
    ret["controls"] = [m_id for m_id, w in control_widgets.items()]

    # What we do is a product(matrix) per output widget
    # with only the ones it affects

    # 1. Iterate the widgets and list which ones it affects

    affected_by = {m_id: set() for m_id, w in value_widgets.items()}

    for w_id, widget in control_widgets.items():
        init_state = get_state(value_widgets)
        widget_possible_values = possible_values(widget)
        affects = []
        # raise Exception(widget)
        for possible_value in widget_possible_values:
            set_widget_value(widget, 1)
            raise Exception(out.outputs)
            # raise Exception(widget)
            # set_widget_value(widget, possible_value)
            # try:
            #     set_widget_value(widget, possible_value)
            # except:
            #     raise Exception((widget, widget_possible_values, possible_value))

            new_state = get_state(value_widgets, b=True)
            diff = diff_state(init_state, new_state, my_id=w_id)
            # raise Exception(widget, diff)
            raise Exception(diff, init_state, new_state)
            # if isinstance(widget, Output):
            #     raise Exception(diff, init_state, new_state)
            # raise Exception(widget_possible_values)
            affects.extend(diff)

        for affected in affects:
            affected_by[affected] = affected_by[affected] | {w_id}

    # 2. Iterate affected_by and add matrix (per output widget) to the matrix

    # matrices = {output_id: [[ ... matrix ... ]] }
    matrices = {}

    for output_widget_id, input_widget_ids in affected_by.items():
        output_widget = all_widgets[output_widget_id]
        if len(input_widget_ids) > 0:
            input_widgets = {m_id: all_widgets[m_id] for m_id in input_widget_ids}
            input_ids = list(input_widgets.keys())
            # return input_widgets
            values = widgets_matrix(input_widgets, output_widget)
            matrices[output_widget_id] = {"affected_by": input_ids, "values": values}

    # return matrices

    ret["onchange"] = matrices
    return json.dumps(ret)


def widgets_matrix(output_widget_id, input_widget_ids):
    """
    Takes a list of input_widgets (model_id, widget_obj)
    and return a matrix of all possible possible values per widget

    Returns
    ------
        dictionary of { "[... inputs_value ... ]": output_value, ... }
    """
    all_widgets = Widget.widgets
    output_widget = all_widgets[output_widget_id]
    input_widgets = {m_id: all_widgets[m_id] for m_id in input_widget_ids}

    # 1. We generate a product of all the possible widget values

    # For each input_widgets, get all possible values they can have
    possible_values_by_widget = {}
    for model_id, widget in input_widgets.items():
        possible_values_by_widget[model_id] = possible_values(widget)

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
        for i, (model_id, value) in enumerate(zip(input_widgets.keys(), inputs_set)):
            # print(i, model_id, value)
            set_widget_value(input_widgets[model_id], value)

        # Save the new value of the output widget
        # print(hash_fn(input_widgets))
        matrix[hash_fn(input_widgets)] = get_widget_output(output_widget)

    return matrix
