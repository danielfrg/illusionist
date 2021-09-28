import ipywidgets as W
import pytest

import illusionist.widgets as IW
from illusionist.preprocessor import possible_values


@pytest.mark.parametrize("class_", IW.NUMERIC_SINGLEVALUE_CONTROL_WIDGETS)
def test_possible_values_num_singlevalue(class_):
    w = class_(min=1, max=5)
    w_state = w.get_state()
    assert possible_values(w_state) == [1, 2, 3, 4, 5]

    w = class_(min=-3, max=2)
    w_state = w.get_state()
    assert possible_values(w_state) == [-3, -2, -1, 0, 1, 2]


@pytest.mark.parametrize("class_", IW.NUMERIC_MULTIVALUE_CONTROL_WIDGETS)
def test_possible_values_num_multivalue(class_):
    w = class_(min=0, max=3)
    w_state = w.get_state()
    a = [
        [0, 0],
        [0, 1],
        [0, 2],
        [0, 3],
        [1, 1],
        [1, 2],
        [1, 3],
        [2, 2],
        [2, 3],
        [3, 3],
    ]
    assert possible_values(w_state) == a


@pytest.mark.parametrize("class_", IW.BOOLEAN_CONTROL_WIDGETS)
def test_possible_values_bool(class_):
    w = class_()
    w_state = w.get_state()
    assert possible_values(w_state) == [True, False]


@pytest.mark.parametrize("class_", IW.SELECTION_SINGLEVALUE_CONTROL_WIDGETS)
def test_possible_values_selection_singlevalue(class_):
    options = ["a", "b", "c"]
    w = class_(options=options)
    w_state = w.get_state()
    assert possible_values(w_state) == [0, 1, 2]

    options = [("One", 1), ("Two", 2), ("Three", 3)]
    w = class_(options=options)
    w_state = w.get_state()
    assert possible_values(w_state) == [0, 1, 2]


@pytest.mark.parametrize("class_", [W.SelectionRangeSlider])
def test_possible_values_selection_multivalue_1(class_):
    options = ["a", "b", "c"]
    w = class_(options=options)
    w_state = w.get_state()
    a = [[0, 0], [0, 1], [0, 2], [1, 1], [1, 2], [2, 2]]
    assert possible_values(w_state) == a


@pytest.mark.parametrize("class_", [W.SelectMultiple])
def test_possible_values_selection_multivalue_2(class_):
    options = ["a"]
    w = class_(options=options)
    w_state = w.get_state()
    assert possible_values(w_state) == [(), (0,)]

    options = ["a", "b"]
    w = class_(options=options)
    w_state = w.get_state()
    assert possible_values(w_state) == [(), (0,), (1,), (0, 1)]

    options = ["a", "b", "c"]
    w = class_(options=options)
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
