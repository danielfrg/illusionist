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
    # BoundedFloatText,  # Floats suck
    # IntText,  # No open ended
    # FloatText,  # No open ended
)
NUMERIC_OUPUT_WIDGETS = (IntProgress, FloatProgress)

BOOLEAN_CONTROL_WIDGETS = (ToggleButton, Checkbox)
BOOLEAN_OUTPUT_WIDGETS = (Valid,)

SELECTION_CONTROL_WIDGETS = (
    Dropdown,
    RadioButtons,
    Select,
    SelectionSlider,
    ToggleButtons,
    SelectMultiple,
    # SelectionRangeSlider,  # TODO
)
SELECTION_OUTPUT_WIDGETS = ()

STRING_CONTROL_WIDGETS = ()
# STRING_CONTROL_WIDGETS = (Text, Textarea)
STRING_OUTPUT_WIDGETS = (Label,)
# STRING_OUTPUT_WIDGETS = (Label, HTML, HTMLMath, Image)

OTHER_CONTROL_WIDGETS = ()
# OTHER_CONTROL_WIDGETS = (Button, Play, DatePicker, ColorPicker)

CONTROL_WIDGETS = (
    NUMERIC_CONTROL_WIDGETS
    + BOOLEAN_CONTROL_WIDGETS
    + SELECTION_CONTROL_WIDGETS
    + STRING_CONTROL_WIDGETS
    + OTHER_CONTROL_WIDGETS
)

OUTPUT_WIDGETS = (
    NUMERIC_OUPUT_WIDGETS
    + BOOLEAN_OUTPUT_WIDGETS
    + SELECTION_OUTPUT_WIDGETS
    + STRING_OUTPUT_WIDGETS
    # + (Output,)
)

VALUE_WIDGETS = CONTROL_WIDGETS + OUTPUT_WIDGETS
LAYOUT_WIDGETS = Box, HBox, VBox, Accordion, Tab


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


def possible_values(widget):
    """
    Returns a list with the possible values for a widget
    """
    if isinstance(widget, (IntSlider, BoundedIntText)):
        return list(range(widget.min, widget.max + widget.step, widget.step))
    if isinstance(widget, (IntRangeSlider,)):
        range_ = range(widget.min, widget.max + widget.step, widget.step)
        list_ = itertools.product(range_, range_)
        list_ = [[i, j] for i, j in list_ if i <= j]
        return list_
    elif isinstance(widget, BOOLEAN_CONTROL_WIDGETS):
        return [True, False]
    elif isinstance(
        widget, (Dropdown, RadioButtons, Select, SelectionSlider, ToggleButtons)
    ):
        if isinstance(widget.options[0], (list, tuple)):
            return [v for k, v in widget.options]
        else:
            return widget.options
    elif isinstance(widget, SelectMultiple):
        return list(powerset(widget.options))
    else:
        widget_type = type(widget)
        raise Exception(f"Widget type 'f{widget_type}' not supported.")


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
    Like `range` but with floats as inputs

    This is stupid and i bet its broken in a lot of ways
    From: https://stackoverflow.com/questions/7267226/range-for-floats
    """
    multiplier = 10 * (y - x) / z
    min_ = int(x * multiplier)
    max_ = int(y * multiplier)
    step_ = int(z * multiplier)
    # print(min_, max_, step_)
    return [x / multiplier for x in range(min_, max_ + step_, step_)]


def generate_onchange(widgets=None):
    all_widgets = get_widgets(widgets=widgets)
    value_widgets = get_widgets(widgets=widgets, kind="value")
    control_widgets = get_widgets(widgets=widgets, kind="control")

    out = {"version_major": 1, "version_minor": 0}
    out["all"] = [m_id for m_id, w in value_widgets.items()]
    out["controls"] = [m_id for m_id, w in control_widgets.items()]

    # What we do is a product(matrix) per output widget
    # with only the ones it affects

    # 1. Iterate the widgets and list which ones it affects

    affected_by = {m_id: set() for m_id, w in value_widgets.items()}

    for w_id, widget in control_widgets.items():
        initial_values = get_state(value_widgets)
        pos_widget_values = possible_values(widget)
        affects = []
        for new_value in pos_widget_values:
            try:
                widget.value = new_value  # Change widget value
            except:
                raise Exception((widget, pos_widget_values, new_value))

            new_values = get_state(get_widgets(widgets=widgets, kind="value"))
            affects.extend(diff_state(initial_values, new_values, my_id=w_id))

        for affected in affects:
            affected_by[affected] = affected_by[affected] | {w_id}

    # 2. Iterate affected_by and generate one matrix per output widget

    # matrix = {output_id: [[ ... matrix ... ]] }
    matrix = {}

    for output_widget_id, input_widget_ids in affected_by.items():
        output_widget = all_widgets[output_widget_id]
        if len(input_widget_ids) > 0:
            input_widgets = {m_id: all_widgets[m_id] for m_id in input_widget_ids}
            input_ids = list(input_widgets.keys())
            # return input_widgets
            values = widgets_matrix(input_widgets, output_widget)
            matrix[output_widget_id] = {"affected_by": input_ids, "values": values}

    # return matrix

    out["onchange"] = matrix
    return json.dumps(out)


def get_state(widgets):
    """
    Get the state of the widgets
    """
    ret = {}
    for model_id, widget in widgets.items():
        ret[model_id] = widget.value
    return ret


def diff_state(initial, new, my_id=None):
    """
    Return a list of widget model_ids that have changed based on the states
    """
    diff = []
    for (initial_id, initial_value), (new_id, new_value) in zip(
        initial.items(), new.items()
    ):
        assert initial_id == new_id
        if initial_value != new_value:
            diff.append(initial_id)

    if my_id and my_id in diff:
        diff.remove(my_id)
    return diff


def widgets_matrix(input_widgets, output_widget):
    """
    Takes a list of input_widgets (model_id, widget_obj)
    and return a matrix of all possible possible values per widget

    Returns
    ------
        dictionary of { "[... inputs_value ... ]": output_value, ... }
    """
    import itertools

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
    input_ids = list()
    for inputs_set in product:

        # Update values of input widgets
        for i, (model_id, value) in enumerate(zip(input_widgets.keys(), inputs_set)):
            # print(i, model_id, value)
            input_widgets[model_id].value = value

        # Save the new value of the output widget
        # print(hash_fn(input_widgets))
        matrix[hash_fn(input_widgets)] = output_widget.value

    return matrix


def hash_fn(widgets):
    values = []
    for model_id, widget in widgets.items():
        if isinstance(widget, NUMERIC_CONTROL_WIDGETS):
            value = widget.value
        if isinstance(widget, BOOLEAN_CONTROL_WIDGETS):
            value = widget.value
        elif isinstance(widget, SELECTION_CONTROL_WIDGETS):
            value = widget.index

        if isinstance(value, str):
            value = json.dumps(value)
        elif isinstance(value, bool):
            value = json.dumps(value)
        elif isinstance(value, tuple):
            value = list(value)
            value = json.dumps(value, separators=(",", ":"))
        # print(value, json.dumps(value))
        # print(type(value), type(json.dumps(value)))
        values.append(value)
    # print(values)
    return dumps(values)


def dumps(values):
    import io
    import csv

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
    # return json.dumps(obj, separators=(",", ":"))
