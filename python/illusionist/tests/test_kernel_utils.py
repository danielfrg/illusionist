import pytest
import ipywidgets
from illusionist import kernel_utils as ku


@pytest.mark.parametrize(
    "class_",
    [
        ipywidgets.Dropdown,
        ipywidgets.RadioButtons,
        ipywidgets.Select,
        ipywidgets.SelectionSlider,
        ipywidgets.ToggleButtons,
    ],
)
def test_get_widget_value_selection(class_):
    options = ["a", "b"]
    w = class_(options=options)
    assert ku.get_widget_output(w) == 0

    w.value = "b"
    assert ku.get_widget_output(w) == 1


@pytest.mark.parametrize(
    "class_", [ipywidgets.SelectMultiple],
)
def test_get_widget_value_selection_multi_value(class_):
    options = ["a", "b"]
    w = class_(options=options)
    assert ku.get_widget_output(w) == []

    w.index = [0]
    assert ku.get_widget_output(w) == [0]
    w.index = [1]
    assert ku.get_widget_output(w) == [1]
    w.index = [0, 1]
    assert ku.get_widget_output(w) == [0, 1]
