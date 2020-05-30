import pytest
import ipywidgets
from illusionist import kernel_utils as ku


@pytest.mark.parametrize("class_", [ipywidgets.IntSlider, ipywidgets.BoundedIntText])
def test_possible_values_int_single_value(class_):
    w = class_(min=1, max=5)
    assert ku.possible_values(w) == [1, 2, 3, 4, 5]

    w = class_(min=-3, max=2)
    assert ku.possible_values(w) == [-3, -2, -1, 0, 1, 2]


def test_possible_values_IntRangeSlider():
    w = ipywidgets.IntRangeSlider(min=0, max=3)
    a = [[0, 0], [0, 1], [0, 2], [0, 3], [1, 1], [1, 2], [1, 3], [2, 2], [2, 3], [3, 3]]
    assert ku.possible_values(w) == a


@pytest.mark.parametrize("class_", [ipywidgets.ToggleButton, ipywidgets.Checkbox])
def test_possible_values_boolean(class_):
    w = class_()
    assert ku.possible_values(w) == [True, False]


def test_widget_matrix_IntSlider():
    slider = ipywidgets.IntSlider()
    label = ipywidgets.Label()
    in_ = {w.model_id: w for w in [slider]}
    matrix = ku.widgets_matrix(in_, label)
    assert list(matrix.keys()) == [str(_) for _ in ku.possible_values(slider)]


def test_widget_matrix_IntRangeSlider():
    slider = ipywidgets.IntRangeSlider(min=0, max=4)
    label = ipywidgets.Label()
    in_ = {w.model_id: w for w in [slider]}
    matrix = ku.widgets_matrix(in_, label)
    ans = [str(_).replace(" ", "") for _ in ku.possible_values(slider)]
    assert list(matrix.keys()) == ans
