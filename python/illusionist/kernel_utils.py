# This code is executed on the Kernel that also executes the notebook

from ipywidgets import *  # noqa


INPUT_NUMERIC_WIDGETS = (
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

INPUT_BOOLEAN_WIDGETS = (ToggleButton, Checkbox)
OUTPUT_BOOLEAN_WIDGETS = (Valid,)

INPUT_SELECTION_WIDGETS = (
    Dropdown,
    RadioButtons,
    Select,
    SelectionSlider,
    SelectionRangeSlider,
    ToggleButtons,
    SelectMultiple,
)
OUTPUT_SELECTION_WIDGETS = ()

INPUT_STRING_WIDGETS = (Text, Textarea)
OUTPUT_STRING_WIDGETS = (Label, HTML, HTMLMath, Image)

OTHER_INPUT_WIDGETS = (Button, Play, DatePicker, ColorPicker)

INPUT_WIDGETS = (
    INPUT_NUMERIC_WIDGETS
    + INPUT_BOOLEAN_WIDGETS
    + INPUT_SELECTION_WIDGETS
    + INPUT_STRING_WIDGETS
)
OUTPUT_WIDGETS = (
    (Output,)
    + OUTPUT_NUMERIC_WIDGETS
    + OUTPUT_BOOLEAN_WIDGETS
    + OUTPUT_SELECTION_WIDGETS
    + OUTPUT_STRING_WIDGETS
)
VALUE_WIDGETS = INPUT_WIDGETS + OUTPUT_WIDGETS

LAYOUT_WIDGETS = Box, HBox, VBox, Accordion, Tab


def get_all_widgets():
    import ipywidgets as widgets

    return widgets.Widget.widgets


def generate_json():
    import json

    all_widgets = get_all_widgets()

    out = {"version_major": 1, "version_minor": 0, "onchange": {}}

    value_widgets = {}
    input_widgets = {}
    for model_id, obj in all_widgets.items():
        if isinstance(obj, VALUE_WIDGETS):
            value_widgets[model_id] = obj
        if isinstance(obj, INPUT_WIDGETS):
            input_widgets[model_id] = obj

    out["onchange"]["targets"] = [mid for mid, w in value_widgets.items()]

    # Iterate combinations and get output values
    input_widgets_product = list(iterate_widgets(input_widgets))
    product = {}
    for combination in input_widgets_product:
        set_widget_values(combination)
        product[hash_fn(combination)] = {i: w.value for i, w in value_widgets.items()}

    out["onchange"]["values"] = product

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
