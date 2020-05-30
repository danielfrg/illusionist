import pytest
import ipywidgets
from illusionist import kernel_utils as ku


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
