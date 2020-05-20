# This code is executed on the Kernel that also executes the notebook

from ipywidgets import *  # noqa


CONTROL_NUMERIC_WIDGETS = (
    IntSlider,
    FloatSlider,
    FloatLogSlider,
    IntRangeSlider,
    FloatRangeSlider,
    BoundedIntText,
    BoundedFloatText,
    IntText,
    FloatText,
)
OUTPUT_NUMERIC_WIDGETS = (IntProgress, FloatProgress)

CONTROL_BOOLEAN_WIDGETS = (ToggleButton, Checkbox)
OUTPUT_BOOLEAN_WIDGETS = (Valid,)

CONTROL_SELECTION_WIDGETS = (
    Dropdown,
    RadioButtons,
    Select,
    SelectionSlider,
    SelectionRangeSlider,
    ToggleButtons,
    SelectMultiple,
)
OUTPUT_SELECTION_WIDGETS = ()

CONTROL_STRING_WIDGETS = (Text, Textarea)
OUTPUT_STRING_WIDGETS = (Label, HTML, HTMLMath, Image)

OTHER_CONTROL_WIDGETS = (Button, Play, DatePicker, ColorPicker)

CONTROL_WIDGETS = (
    CONTROL_NUMERIC_WIDGETS
    + CONTROL_BOOLEAN_WIDGETS
    + CONTROL_SELECTION_WIDGETS
    + CONTROL_STRING_WIDGETS
)
OUTPUT_WIDGETS = (
    (Output,)
    + OUTPUT_NUMERIC_WIDGETS
    + OUTPUT_BOOLEAN_WIDGETS
    + OUTPUT_SELECTION_WIDGETS
    + OUTPUT_STRING_WIDGETS
)
VALUE_WIDGETS = CONTROL_WIDGETS + OUTPUT_WIDGETS

LAYOUT_WIDGETS = Box, HBox, VBox, Accordion, Tab


def get_all_widgets():
    import ipywidgets as widgets

    return widgets.Widget.widgets


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
            control_widgets[model_id] = obj

    out["controls"] = [mid for mid, w in control_widgets.items()]
    # out["targets"] = [mid for mid, w in value_widgets.items()]

    # Iterate combinations and get output values
    control_widgets_product = list(iterate_widgets(control_widgets))
    product = {}
    for one_set in control_widgets_product:
        set_widget_values(one_set)
        product[hash_fn(one_set)] = {i: w.value for i, w in value_widgets.items()}

    out["values"] = product

    return json.dumps(out)


def set_widget_values(combination):
    import ipywidgets as widgets

    all_widgets = widgets.Widget.widgets

    for widget_info in combination:
        model_id = widget_info.split("=")[0]
        value = "".join(widget_info.split("=")[1:])
        all_widgets[model_id].value = value


def iterate_widgets(widgets):
    import itertools

    # For all the widgets, get all possible values in a list
    # They list items are keys of {model_id-value}
    possible_values_by_widget = {}
    for model_id, obj in widgets.items():
        possible_values_by_widget[model_id] = possible_values(obj)

    list_ = possible_values_by_widget.values()
    return itertools.product(*list_)


def possible_values(widget):
    model_id = widget.model_id
    values = []
    for value in range(widget.min, widget.max + widget.step, widget.step):
        key = f"{model_id}={value}"
        values.append(key)
    return values


def hash_fn(widgets):
    return ",".join(widgets)
    # import json
    # values = {}
    # for model_id, obj in widgets.items():
    #     values[model_id] = obj.value

    # str_val = json.dumps(values)
    # return hash(str_val)
