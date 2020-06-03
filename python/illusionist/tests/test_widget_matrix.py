import ipywidgets
import pytest

from illusionist.preprocessor import possible_values
from illusionist.widgets import *  # noqa

from .utils import preprocessor


def test_widget_matrix_IntSlider(preprocessor):
    preprocessor.run_code("w = IntSlider(min=-3, max=0)")
    preprocessor.run_code("lbl = Label()")
    in_id = preprocessor.run_code_eval("w.model_id")
    out_id = preprocessor.run_code_eval("lbl.model_id")
    in_ids = [in_id]

    matrix = preprocessor.widget_matrix(out_id, in_ids)
    assert list(matrix.keys()) == ["-3", "-2", "-1", "0"]


def test_widget_matrix_IntRangeSlider(preprocessor):
    preprocessor.run_code("w = IntRangeSlider(min=0, max=2)")
    preprocessor.run_code("lbl = Label()")
    in_id = preprocessor.run_code_eval("w.model_id")
    out_id = preprocessor.run_code_eval("lbl.model_id")
    in_ids = [in_id]

    matrix = preprocessor.widget_matrix(out_id, in_ids)
    ans = ['"[0,0]"', '"[0,1]"', '"[0,2]"', '"[1,1]"', '"[1,2]"', '"[2,2]"']
    assert list(matrix.keys()) == ans


@pytest.mark.parametrize(
    "class_",
    [
        # "Dropdown",
        # "RadioButtons",
        # "Select",
        # "SelectionSlider",
        # "ToggleButtons",
        "SelectMultiple",
    ],
)
def test_widget_matrix_Selection(preprocessor, class_):
    preprocessor.run_code(f'w = {class_}(options=["a", "b", "c"])')
    preprocessor.run_code("lbl = Label()")
    in_id = preprocessor.run_code_eval("w.model_id")
    out_id = preprocessor.run_code_eval("lbl.model_id")
    in_ids = [in_id]

    matrix = preprocessor.widget_matrix(out_id, in_ids)
    ans = [
        '"[]"',
        '"[0]"',
        '"[1]"',
        '"[2]"',
        '"[0,1]"',
        '"[0,2]"',
        '"[1,2]"',
        '"[0,1,2]"',
    ]
    assert list(matrix.keys()) == ans
