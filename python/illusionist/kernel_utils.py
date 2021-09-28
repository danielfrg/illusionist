# This module is executed on the Kernel that also executes the notebook

try:
    # This will fail when executed in the Kernel is just for linting purposes
    import ipywidgets as W

    from .widgets import (
        BOOLEAN_OUTPUT_WIDGETS,
        CONTROL_WIDGETS,
        NUMERIC_OUTPUT_WIDGETS,
        SELECTION_OUTPUT_WIDGETS,
        STRING_OUTPUT_WIDGETS,
        VALUE_WIDGETS,
    )
except:
    pass


def get_widgets_ids(widgets=None, kind=None):
    """
    Return all widgets that are used in the notebook
    Parameters
    ----------
        widgets (list): List of widgets to
    Returns
    -------
        dictionary of `{"model_id": widget_object}`
    """
    # The `Widgets` class has a registry of all the widgets that were used
    all_widgets = widgets if widgets else W.Widget.widgets

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


def set_widget_value(widget_id, value):
    """
    Set the value of a widget
    """
    widget = W.Widget.widgets[widget_id]
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
