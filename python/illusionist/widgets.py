# A module that imports all ipywidgets

import ipywidgets as W

NUMERIC_CONTROL_WIDGETS = (
    W.IntSlider,
    # FloatSlider,  # floats not supported
    # FloatLogSlider,  # floats not supported
    W.IntRangeSlider,
    # FloatRangeSlider,  # floats not supported
    W.BoundedIntText,
    # BoundedFloatText,  # floats not supported
    # IntText,  # open ended widgets not supported
    # FloatText,  # open ended widgets not supported
)
NUMERIC_OUTPUT_WIDGETS = NUMERIC_CONTROL_WIDGETS + (
    W.IntProgress,
    W.FloatProgress,
)

BOOLEAN_CONTROL_WIDGETS = (W.ToggleButton, W.Checkbox)
BOOLEAN_OUTPUT_WIDGETS = BOOLEAN_CONTROL_WIDGETS + (W.Valid,)

SELECTION_SINGLE_CONTROL_WIDGETS = (
    W.Dropdown,
    W.RadioButtons,
    W.Select,
    W.SelectionSlider,
    W.ToggleButtons,
)
SELECTION_MULTIPLE_CONTROL_WIDGETS = (
    W.SelectionRangeSlider,
    W.SelectMultiple,
)
SELECTION_CONTROL_WIDGETS = (
    SELECTION_SINGLE_CONTROL_WIDGETS + SELECTION_MULTIPLE_CONTROL_WIDGETS
)
SELECTION_OUTPUT_WIDGETS = SELECTION_CONTROL_WIDGETS

STRING_CONTROL_WIDGETS = (
    # Text,  # open ended widgets not supported
    # Textarea,  # open ended widgets not supported
)
STRING_OUTPUT_WIDGETS = (
    W.Label,
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
    + (W.Output,)
)

VALUE_WIDGETS = CONTROL_WIDGETS + OUTPUT_WIDGETS
LAYOUT_WIDGETS = (W.Box, W.HBox, W.VBox, W.Accordion, W.Tab)
