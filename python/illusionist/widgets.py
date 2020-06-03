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
