# This code is executed on the Kernel that also executes the notebook
import itertools
import json

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
