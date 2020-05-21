# This code is executed on the Kernel that also executes the notebook

from ipywidgets import *  # noqa


NUMERIC_CONTROL_WIDGETS = (
    IntSlider,
    FloatSlider,
    # FloatLogSlider,
    IntRangeSlider,
    FloatRangeSlider,
    BoundedIntText,
    BoundedFloatText,
    # IntText,
    # FloatText,
)
NUMERIC_OUPUT_WIDGETS = (IntProgress, FloatProgress)

BOOLEAN_CONTROL_WIDGETS = (ToggleButton, Checkbox)
BOOLEAN_OUTPUT_WIDGETS = (Valid,)

SELECTION_CONTROL_WIDGETS = (
    Dropdown,
    RadioButtons,
    Select,
    SelectionSlider,
    # SelectionRangeSlider,
    ToggleButtons,
    SelectMultiple,
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
    + (Output,)
)

VALUE_WIDGETS = CONTROL_WIDGETS + OUTPUT_WIDGETS
LAYOUT_WIDGETS = Box, HBox, VBox, Accordion, Tab

def get_all_widgets():
    """
    Return all widgets that are used in the notebook
    """
    import ipywidgets as widgets
    # The `Widgets` class has a registry of all the widgets that were used
    return widgets.Widget.widgets


def possible_values(widget):
    """
    Returns a list with the possible values for a widget
    """
    # model_id = widget.model_id

    if isinstance(widget, (IntSlider, IntRangeSlider, BoundedIntText)):
        return list(range(widget.min, widget.max + widget.step, widget.step))
    elif isinstance(widget, (FloatSlider, FloatRangeSlider, BoundedFloatText)):
        return frange(widget.min, widget.max, widget.step)
    elif isinstance(widget, FloatLogSlider):
        # TODO: quick maths
        return []
    elif isinstance(widget, BOOLEAN_CONTROL_WIDGETS):
        return [True, False]
    elif isinstance(widget, SELECTION_CONTROL_WIDGETS):
        return widget.options
    else:
        widget_type = type(widget)
        raise Exception(f"Widget type 'f{widget_type}' not supported.")


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


def generate_json():
    import json

    all_widgets = get_all_widgets()

    out = {"version_major": 1, "version_minor": 0}

    value_widgets = {}
    control_widgets = {}
    for model_id, obj in all_widgets.items():
        if isinstance(obj, VALUE_WIDGETS):
            value_widgets[model_id] = obj
        if isinstance(obj, CONTROL_WIDGETS):
            if not obj.disabled:
                control_widgets[model_id] = obj

    out["controls"] = [mid for mid, w in control_widgets.items()]
    out["all"] = [mid for mid, w in value_widgets.items()]

    # Iterate combinations and get output values
    control_widgets_product = list(widgets_product(control_widgets))
    return control_widgets_product

    # product = {}
    # for one_set in control_widgets_product:
    #     set_widget_values(one_set)
    #     product[hash_fn(one_set)] = {i: w.value for i, w in value_widgets.items()}

    # out["values"] = product

    # return json.dumps(out)


def widgets_product(widgets):
    """
    Takes a list of widgets and makes a product of all the possible possible values per widget
    """
    import itertools

    # For all the widgets, get all possible values in a list
    # They list items are keys of {model_id-value}
    possible_values_by_widget = {}
    for model_id, obj in widgets.items():
        possible_values_by_widget[model_id] = possible_values(obj)
        # raise Exception(possible_values_by_widget[model_id])
        print(possible_values_by_widget[model_id])

    list_ = possible_values_by_widget.values()
    return list_
    return itertools.product(*list_)


def set_widget_values(combination):
    import ipywidgets as widgets

    all_widgets = widgets.Widget.widgets

    for widget_info in combination:
        model_id = widget_info.split("=")[0]
        value = "".join(widget_info.split("=")[1:])
        all_widgets[model_id].value = value


def hash_fn(widgets):
    return ",".join(widgets)
    # import json
    # values = {}
    # for model_id, obj in widgets.items():
    #     values[model_id] = obj.value

    # str_val = json.dumps(values)
    # return hash(str_val)
