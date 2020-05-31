import pytest
import ipywidgets
from illusionist import kernel_utils as ku


@pytest.mark.parametrize("class_", [ipywidgets.IntSlider, ipywidgets.BoundedIntText])
def test_possible_values_int_single_value(class_):
    w = class_(min=1, max=5)
    assert ku.possible_values(w) == [1, 2, 3, 4, 5]

    w = class_(min=-3, max=2)
    assert ku.possible_values(w) == [-3, -2, -1, 0, 1, 2]


def test_possible_values_int_multi_value():
    w = ipywidgets.IntRangeSlider(min=0, max=3)
    a = [[0, 0], [0, 1], [0, 2], [0, 3], [1, 1], [1, 2], [1, 3], [2, 2], [2, 3], [3, 3]]
    assert ku.possible_values(w) == a


@pytest.mark.parametrize("class_", [ipywidgets.ToggleButton, ipywidgets.Checkbox])
def test_possible_values_boolean(class_):
    w = class_()
    assert ku.possible_values(w) == [True, False]


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
def test_possible_values_selection_single_value(class_):
    options = ["a", "b", "c"]
    w = class_(options=options)
    assert ku.possible_values(w) == [0, 1, 2]

    options = [("One", 1), ("Two", 2), ("Three", 3)]
    w = class_(options=options)
    assert ku.possible_values(w) == [0, 1, 2]


def test_possible_values_SelectMultiple():
    options = ["a"]
    w = ipywidgets.SelectMultiple(options=options)
    assert ku.possible_values(w) == [(), (0,)]

    options = ["a", "b"]
    w = ipywidgets.SelectMultiple(options=options)
    assert ku.possible_values(w) == [(), (0,), (1,), (0, 1)]

    options = ["a", "b", "c"]
    w = ipywidgets.SelectMultiple(options=options)
    assert ku.possible_values(w) == [
        (),
        (0,),
        (1,),
        (2,),
        (0, 1),
        (0, 2),
        (1, 2),
        (0, 1, 2),
    ]


def test_possible_values_SelectionRangeSlider():
    options = ["a", "b", "c"]
    w = ipywidgets.SelectionRangeSlider(options=options)
    a = [[0, 0], [0, 1], [0, 2], [1, 1], [1, 2], [2, 2]]
    assert ku.possible_values(w) == a
