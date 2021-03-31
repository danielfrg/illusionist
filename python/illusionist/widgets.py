import ipywidgets as W


NUMERIC_CONTROL_WIDGETS = (
    W.IntSlider,
    # FloatSlider,  # floats suck
    # FloatLogSlider,  # floats suck
    W.IntRangeSlider,
    # FloatRangeSlider,  # floats suck
    W.BoundedIntText,
    # BoundedFloatText,  # floats suck
    # IntText,  # No open ended
    # FloatText,  # No open ended
)
NUMERIC_OUTPUT_WIDGETS = NUMERIC_CONTROL_WIDGETS + (W.IntProgress, W.FloatProgress)

BOOLEAN_CONTROL_WIDGETS = (W.ToggleButton, W.Checkbox)
BOOLEAN_OUTPUT_WIDGETS = BOOLEAN_CONTROL_WIDGETS + (W.Valid,)

SELECTION_CONTROL_WIDGETS = (
    W.Dropdown,
    W.RadioButtons,
    W.Select,
    W.SelectionSlider,
    W.ToggleButtons,
    W.SelectionRangeSlider,
    W.SelectMultiple,
)
SELECTION_OUTPUT_WIDGETS = SELECTION_CONTROL_WIDGETS

STRING_CONTROL_WIDGETS = (
    # Text,  # No open ended
    # Textarea,  # No opeen ended
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
LAYOUT_WIDGETS = W.Box, W.HBox, W.VBox, W.Accordion, W.Tab
