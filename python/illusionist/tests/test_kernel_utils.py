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
    assert ku.possible_values(w) == w.options

    options = [("One", 1), ("Two", 2), ("Three", 3)]
    w = class_(options=options)
    assert ku.possible_values(w) == [1, 2, 3]


@pytest.mark.parametrize(
    "class_", [ipywidgets.SelectMultiple],
)
def test_possible_values_selection_multi_value(class_):
    options = ["a"]
    w = class_(options=options)
    assert ku.possible_values(w) == [(), ("a",)]

    options = ["a", "b"]
    w = class_(options=options)
    assert ku.possible_values(w) == [(), ("a",), ("b",), ("a", "b")]

    options = ["a", "b", "c"]
    w = class_(options=options)
    assert ku.possible_values(w) == [
        (),
        ("a",),
        ("b",),
        ("c",),
        ("a", "b"),
        ("a", "c"),
        ("b", "c"),
        ("a", "b", "c"),
    ]


@pytest.mark.parametrize("class_", [ipywidgets.IntSlider, ipywidgets.BoundedIntText])
def test_hash_fn_int_single_value(class_):
    w = class_(min=1, max=5)
    inputs = {w.model_id: w for w in [w]}
    assert ku.hash_fn(inputs) == "1"

    w.value = 5
    assert ku.hash_fn(inputs) == "5"


@pytest.mark.parametrize("class_", [ipywidgets.IntSlider, ipywidgets.BoundedIntText])
def test_hash_fn_int_multiple_single_value(class_):
    w1 = class_(min=1, max=5)
    w2 = class_(min=6, max=10)
    inputs = {w.model_id: w for w in [w1, w2]}
    assert ku.hash_fn(inputs) == "1,6"

    w1.value = 5
    w2.value = 8
    assert ku.hash_fn(inputs) == "5,8"


@pytest.mark.parametrize("class_", ku.BOOLEAN_CONTROL_WIDGETS)
def test_hash_fn_boolean(class_):
    w = class_()
    inputs = {w.model_id: w for w in [w]}
    assert ku.hash_fn(inputs) == '"false"'

    w.value = True
    assert ku.hash_fn(inputs) == '"true"'


@pytest.mark.parametrize("class_", ku.BOOLEAN_CONTROL_WIDGETS)
def test_hash_fn_boolean_multiple(class_):
    w1 = class_()
    w2 = class_()
    inputs = {w.model_id: w for w in [w1, w2]}
    assert ku.hash_fn(inputs) == '"false","false"'

    w1.value = True
    assert ku.hash_fn(inputs) == '"true","false"'
    w2.value = True
    assert ku.hash_fn(inputs) == '"true","true"'


@pytest.mark.parametrize(
    "class_", [ipywidgets.SelectMultiple],
)
def test_hash_fn_selection_multi_value(class_):
    options = ["a", "b"]
    w = class_(options=options)
    inputs = {w.model_id: w for w in [w]}
    assert ku.hash_fn(inputs) == '"[]"'

    w.value = ["a"]
    assert ku.hash_fn(inputs) == '"[0]"'

    w.value = ["b"]
    assert ku.hash_fn(inputs) == '"[1]"'

    w.value = ["a", "b"]
    assert ku.hash_fn(inputs) == '"[0,1]"'


# def test_widget_matrix_IntSlider():
#     slider = ipywidgets.IntSlider()
#     label = ipywidgets.Label()
#     in_ = {w.model_id: w for w in [slider]}
#     matrix = ku.widgets_matrix(in_, label)
#     assert list(matrix.keys()) == [str(_) for _ in ku.possible_values(slider)]


# def test_widget_matrix_IntRangeSlider():
#     slider = ipywidgets.IntRangeSlider(min=0, max=4)
#     label = ipywidgets.Label()
#     in_ = {w.model_id: w for w in [slider]}
#     matrix = ku.widgets_matrix(in_, label)
#     ans = [str(_).replace(" ", "") for _ in ku.possible_values(slider)]
#     assert list(matrix.keys()) == ans


# @pytest.mark.parametrize(
#     "class_",
#     [
#         # ipywidgets.Dropdown,
#         # ipywidgets.RadioButtons,
#         # ipywidgets.Select,
#         # ipywidgets.SelectionSlider,
#         # ipywidgets.ToggleButtons,
#         ipywidgets.SelectMultiple,
#     ],
# )
# def test_widget_matrix_Selection(class_):
#     options = ["a", "b", "c"]
#     selection = class_(options=options)
#     label = ipywidgets.Label()
#     in_ = {w.model_id: w for w in [selection]}
#     matrix = ku.widgets_matrix(in_, label)
#     ans = [
#         '"[]"',
#         '"[""a""]"',
#         '"[""b""]"',
#         '"[""c""]"',
#         '"[""a"", ""b""]"',
#         '"[""a"", ""c""]"',
#         '"[""b"", ""c""]"',
#         '"[""a"", ""b"", ""c""]"',
#     ]
#     assert list(matrix.keys()) == ans
