import pytest


def test_static_values_single_IntSlider(preprocessor):
    preprocessor.exec_code("w = W.IntSlider(min=-3, max=0)")
    preprocessor.exec_code("lbl = W.Label()")
    in_id = preprocessor.exec_code("w.model_id")
    in_id = preprocessor.eval_cell(in_id)
    out_id = preprocessor.exec_code("lbl.model_id")
    out_id = preprocessor.eval_cell(out_id)
    in_ids = [in_id]

    matrix = preprocessor.get_static_values_by_widget(out_id, in_ids)
    assert list(matrix.keys()) == ["-3", "-2", "-1", "0"]


def test_static_values_single_IntRangeSlider(preprocessor):
    preprocessor.exec_code("w = W.IntRangeSlider(min=0, max=2)")
    preprocessor.exec_code("lbl = W.Label()")
    in_id = preprocessor.exec_code("w.model_id")
    in_id = preprocessor.eval_cell(in_id)
    out_id = preprocessor.exec_code("lbl.model_id")
    out_id = preprocessor.eval_cell(out_id)
    in_ids = [in_id]

    matrix = preprocessor.get_static_values_by_widget(out_id, in_ids)
    ans = ['"[0,0]"', '"[0,1]"', '"[0,2]"', '"[1,1]"', '"[1,2]"', '"[2,2]"']
    assert list(matrix.keys()) == ans


# @pytest.mark.parametrize(
#     "class_",
#     [
#         # "Dropdown",
#         # "RadioButtons",
#         # "Select",
#         # "SelectionSlider",
#         # "ToggleButtons",
#         "SelectMultiple",
#     ],
# )
# def test_static_values_single_Selection(preprocessor, class_):
#     preprocessor.exec_code(f'w = W.{class_}(options=["a", "b", "c"])')
#     preprocessor.exec_code("lbl = W.Label()")
#     in_id = preprocessor.eval_cell("w.model_id")
#     out_id = preprocessor.eval_cell("lbl.model_id")
#     in_ids = [in_id]

#     matrix = preprocessor.get_static_values_by_widget(out_id, in_ids)
#     ans = [
#         '"[]"',
#         '"[0]"',
#         '"[1]"',
#         '"[2]"',
#         '"[0,1]"',
#         '"[0,2]"',
#         '"[1,2]"',
#         '"[0,1,2]"',
#     ]
#     assert list(matrix.keys()) == ans
