# A module that lists all ipywidgets Model names

NUMERIC_SINGLEVALUE_CONTROL_WIDGETS = (
    "IntSliderModel",
    # "FloatSlider",  # floats not supported
    # "FloatLogSlider",  # floats not supported
    "BoundedIntTextModel",
    # "BoundedFloatText",  # floats not supported
    # "IntText",  # open ended widgets not supported
    # "FloatText",  # open ended widgets not supported
)
NUMERIC_MULTIVALUE_CONTROL_WIDGETS = (
    "IntRangeSliderModel",
    # "FloatRangeSlider",  # floats not supported
)
NUMERIC_CONTROL_WIDGETS = (
    NUMERIC_SINGLEVALUE_CONTROL_WIDGETS + NUMERIC_MULTIVALUE_CONTROL_WIDGETS
)
NUMERIC_OUTPUT_WIDGETS = NUMERIC_CONTROL_WIDGETS + (
    "IntProgressModel",
    "FloatProgressModel",
)

BOOLEAN_CONTROL_WIDGETS = ("ToggleButtonModel", "CheckboxModel")
BOOLEAN_OUTPUT_WIDGETS = BOOLEAN_CONTROL_WIDGETS + ("ValidModel",)

SELECTION_SINGLE_CONTROL_WIDGETS = (
    "DropdownModel",
    "RadioButtonsModel",
    "SelectModel",
    "SelectionSliderModel",
    "ToggleButtonsModel",
)
SELECTION_MULTIPLE_CONTROL_WIDGETS = (
    "SelectionRangeSliderModel",
    "SelectMultipleModel",
)
SELECTION_CONTROL_WIDGETS = (
    SELECTION_SINGLE_CONTROL_WIDGETS + SELECTION_MULTIPLE_CONTROL_WIDGETS
)
SELECTION_OUTPUT_WIDGETS = SELECTION_CONTROL_WIDGETS

STRING_CONTROL_WIDGETS = (
    # "Text",  # open ended widgets not supported
    # "Textarea",  # open ended widgets not supported
)
STRING_OUTPUT_WIDGETS = (
    "LabelModel",
    # "HTMLModel",  # TODO
    # "HTMLMathModel",  # TODO
    # "ImageModel",  # TODO
)

OTHER_CONTROL_WIDGETS = (
    # "ButtonModel",  # TODO
    # "PlayModel",  # TODO
    # "DatePickerModel",  # TODO
    # "ColorPickerModel"  # TODO
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
    + ("OutputModel",)
)

VALUE_WIDGETS = CONTROL_WIDGETS + OUTPUT_WIDGETS
LAYOUT_WIDGETS = (
    "BoxModel",
    "HBoxModel",
    "VBoxModel",
    "AccordionModel",
    "TabModel",
)
