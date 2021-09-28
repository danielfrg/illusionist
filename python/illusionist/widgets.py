# A module that imports all ipywidgets

import ipywidgets as W

NUMERIC_SINGLEVALUE_CONTROL_WIDGETS = (
    W.IntSlider,
    # W.FloatSlider,  # floats not supported
    # W.FloatLogSlider,  # floats not supported
    W.BoundedIntText,
    # W.BoundedFloatText,  # floats not supported
    # W.IntText,  # open ended widgets not supported
    # W.FloatText,  # open ended widgets not supported
)
NUMERIC_MULTIVALUE_CONTROL_WIDGETS = (
    W.IntRangeSlider,
    # W.FloatRangeSlider,  # floats not supported
)
NUMERIC_CONTROL_WIDGETS = (
    NUMERIC_SINGLEVALUE_CONTROL_WIDGETS + NUMERIC_MULTIVALUE_CONTROL_WIDGETS
)
NUMERIC_OUTPUT_WIDGETS = NUMERIC_CONTROL_WIDGETS + (
    W.IntProgress,
    W.FloatProgress,
)

BOOLEAN_CONTROL_WIDGETS = (W.ToggleButton, W.Checkbox)
BOOLEAN_OUTPUT_WIDGETS = BOOLEAN_CONTROL_WIDGETS + (W.Valid,)

SELECTION_SINGLEVALUE_CONTROL_WIDGETS = (
    W.Dropdown,
    W.RadioButtons,
    W.Select,
    W.SelectionSlider,
    W.ToggleButtons,
)
SELECTION_MULTIVALUE_CONTROL_WIDGETS = (
    W.SelectionRangeSlider,
    W.SelectMultiple,
)
SELECTION_CONTROL_WIDGETS = (
    SELECTION_SINGLEVALUE_CONTROL_WIDGETS
    + SELECTION_MULTIVALUE_CONTROL_WIDGETS
)
SELECTION_OUTPUT_WIDGETS = SELECTION_CONTROL_WIDGETS

STRING_CONTROL_WIDGETS = (
    # Text,  # open ended widgets not supported
    # Textarea,  # open ended widgets not supported
)
STRING_OUTPUT_WIDGETS = (
    W.Label,
    # W.HTML,  # TODO
    # W.HTMLMath,  # TODO
    # W.Image,  # TODO
)

OTHER_CONTROL_WIDGETS = (
    # W.Button,  # TODO
    # W.Play,  # TODO
    # W.DatePicker,  # TODO
    # W.ColorPicker  # TODO
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
    + (W.Output,)
)

VALUE_WIDGETS = CONTROL_WIDGETS + OUTPUT_WIDGETS
LAYOUT_WIDGETS = (W.Box, W.HBox, W.VBox, W.Accordion, W.Tab)
