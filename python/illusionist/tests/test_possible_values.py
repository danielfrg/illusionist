import ipywidgets
import pytest

from illusionist.preprocessor import possible_values
from illusionist.widgets import *  # noqa


@pytest.mark.parametrize("class_", [IntSlider, BoundedIntText])
def test_possible_values_int_single_value(class_):
    w = class_(min=1, max=5)
    w_state = w.get_state()
    assert possible_values(w_state) == [1, 2, 3, 4, 5]

    w = class_(min=-3, max=2)
    w_state = w.get_state()
    assert possible_values(w_state) == [-3, -2, -1, 0, 1, 2]


def test_possible_values_IntRangeSlider():
    w = IntRangeSlider(min=0, max=3)
    w_state = w.get_state()
    a = [[0, 0], [0, 1], [0, 2], [0, 3], [1, 1], [1, 2], [1, 3], [2, 2], [2, 3], [3, 3]]
    assert possible_values(w_state) == a


@pytest.mark.parametrize("class_", [ToggleButton, Checkbox])
def test_possible_values_boolean(class_):
    w = class_()
    w_state = w.get_state()
    assert possible_values(w_state) == [True, False]


@pytest.mark.parametrize(
    "class_", [Dropdown, RadioButtons, Select, SelectionSlider, ToggleButtons,],
)
def test_possible_values_selection_single_value(class_):
    options = ["a", "b", "c"]
    w = class_(options=options)
    w_state = w.get_state()
    assert possible_values(w_state) == [0, 1, 2]

    options = [("One", 1), ("Two", 2), ("Three", 3)]
    w = class_(options=options)
    w_state = w.get_state()
    assert possible_values(w_state) == [0, 1, 2]


def test_possible_values_SelectMultiple():
    options = ["a"]
    w = SelectMultiple(options=options)
    w_state = w.get_state()
    assert possible_values(w_state) == [(), (0,)]

    options = ["a", "b"]
    w = SelectMultiple(options=options)
    w_state = w.get_state()
    assert possible_values(w_state) == [(), (0,), (1,), (0, 1)]

    options = ["a", "b", "c"]
    w = SelectMultiple(options=options)
    w_state = w.get_state()
    assert possible_values(w_state) == [
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
    w = SelectionRangeSlider(options=options)
    w_state = w.get_state()
    a = [[0, 0], [0, 1], [0, 2], [1, 1], [1, 2], [2, 2]]
    assert possible_values(w_state) == a


# def test_pb(preprocessor):
# # def test_pb(preprocessor):
#     # preprocessor.run_code("import ipywidgets")
#     # preprocessor.run_code("w = IntSlider(min=5, max=10)")
#     # w_id = preprocessor.run_code_eval("w.model_id")

#     w = IntSlider(min=5, max=10)
#     w_state = w.get_state()
#     # w_id = list(preprocessor.widget_state.keys())[0]
#     assert possible_values(w_state)
#     # print(preprocessor.widget_state)

#     preprocessor._cleanup_kernel()
