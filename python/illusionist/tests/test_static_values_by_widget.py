import ipywidgets as W
import pytest

import illusionist.widgets as IW


@pytest.mark.parametrize("class_", IW.NUMERIC_SINGLEVALUE_CONTROL_WIDGETS)
def test_static_values_byw_num_nolink(preprocessor, class_):
    preprocessor.exec_code(
        f"""
w = W.{class_.__name__}(min=-3, max=0)
lbl = W.Label()
"""
    )
    control_w_id = preprocessor.exec_code("w.model_id")
    control_w_id = preprocessor.eval_cell(control_w_id)
    value_w_id = preprocessor.exec_code("lbl.model_id")
    value_w_id = preprocessor.eval_cell(value_w_id)
    control_w_ids = [control_w_id]

    values = preprocessor.get_static_values_by_widget(
        value_w_id, control_w_ids
    )
    assert list(values.keys()) == ["-3", "-2", "-1", "0"]
    assert list(values.values()) == ["", "", "", ""]


@pytest.mark.parametrize("class_", IW.NUMERIC_SINGLEVALUE_CONTROL_WIDGETS)
def test_static_values_byw_num_link(preprocessor, class_):
    preprocessor.exec_code(
        f"""
w = W.{class_.__name__}(min=-3, max=0)
lbl = W.Label()

def update(args):
    lbl.value = str(w.value * 2)

update(None)
w.observe(update, "value")
"""
    )
    control_w_id = preprocessor.exec_code("w.model_id")
    control_w_id = preprocessor.eval_cell(control_w_id)
    value_w_id = preprocessor.exec_code("lbl.model_id")
    value_w_id = preprocessor.eval_cell(value_w_id)
    control_w_ids = [control_w_id]

    values = preprocessor.get_static_values_by_widget(
        value_w_id, control_w_ids
    )
    assert list(values.keys()) == ["-3", "-2", "-1", "0"]
    assert list(values.values()) == ["-6", "-4", "-2", "0"]


@pytest.mark.parametrize("class_", IW.NUMERIC_MULTIVALUE_CONTROL_WIDGETS)
def test_static_values_byw_num_multivalue_link(preprocessor, class_):
    preprocessor.exec_code(
        f"""
w = W.{class_.__name__}(min=0, max=2)
lbl = W.Label()

def update(args):
    lbl.value = str(w.value[0] + w.value[1])

update(None)
w.observe(update, "value")
"""
    )
    control_w_id = preprocessor.exec_code("w.model_id")
    control_w_id = preprocessor.eval_cell(control_w_id)
    value_w_id = preprocessor.exec_code("lbl.model_id")
    value_w_id = preprocessor.eval_cell(value_w_id)
    control_w_ids = [control_w_id]

    values = preprocessor.get_static_values_by_widget(
        value_w_id, control_w_ids
    )

    ans = ['"[0,0]"', '"[0,1]"', '"[0,2]"', '"[1,1]"', '"[1,2]"', '"[2,2]"']
    assert list(values.keys()) == ans
    assert list(values.values()) == ["0", "1", "2", "2", "3", "4"]


@pytest.mark.parametrize("class_", IW.SELECTION_SINGLEVALUE_CONTROL_WIDGETS)
def test_static_values_byw_selection_singlevalue(preprocessor, class_):
    preprocessor.exec_code(
        f"""
options = ["aa", "bb", "cc", "dd"]
w = W.{class_.__name__}(options=options)
lbl = W.Label()

def update(args):
    lbl.value = str(w.value)

update(None)
w.observe(update, "value")
"""
    )
    control_w_id = preprocessor.exec_code("w.model_id")
    control_w_id = preprocessor.eval_cell(control_w_id)
    value_w_id = preprocessor.exec_code("lbl.model_id")
    value_w_id = preprocessor.eval_cell(value_w_id)
    control_w_ids = [control_w_id]

    values = preprocessor.get_static_values_by_widget(
        value_w_id, control_w_ids
    )

    assert list(values.keys()) == ["0", "1", "2", "3"]
    assert list(values.values()) == ["aa", "bb", "cc", "dd"]


@pytest.mark.parametrize("class_", [W.SelectionRangeSlider])
def test_static_values_byw_selection_multivalue_1(preprocessor, class_):
    preprocessor.exec_code(
        f"""
options = ["a", "b", "c", "d"]
w = W.{class_.__name__}(options=options)
lbl = W.Label()

def update(args):
    lbl.value = str(w.value)

update(None)
w.observe(update, "value")
"""
    )
    control_w_id = preprocessor.exec_code("w.model_id")
    control_w_id = preprocessor.eval_cell(control_w_id)
    value_w_id = preprocessor.exec_code("lbl.model_id")
    value_w_id = preprocessor.eval_cell(value_w_id)
    control_w_ids = [control_w_id]

    values = preprocessor.get_static_values_by_widget(
        value_w_id, control_w_ids
    )

    ans = [
        '"[0,0]"',
        '"[0,1]"',
        '"[0,2]"',
        '"[0,3]"',
        '"[1,1]"',
        '"[1,2]"',
        '"[1,3]"',
        '"[2,2]"',
        '"[2,3]"',
        '"[3,3]"',
    ]
    assert list(values.keys()) == ans
    ans = [
        '()',
        "('a', 'b')",
        "('a', 'c')",
        "('a', 'd')",
        "('b', 'b')",
        "('b', 'c')",
        "('b', 'd')",
        "('c', 'c')",
        "('c', 'd')",
        "('d', 'd')",
    ]
    assert list(values.values()) == ans


@pytest.mark.parametrize("class_", [W.SelectMultiple])
def test_static_values_byw_selection_multivalue_2(preprocessor, class_):
    preprocessor.exec_code(
        f"""
options = ["a", "b", "c"]
w = W.{class_.__name__}(options=options)
lbl = W.Label()

def update(args):
    lbl.value = str(w.value)

update(None)
w.observe(update, "value")
"""
    )
    control_w_id = preprocessor.exec_code("w.model_id")
    control_w_id = preprocessor.eval_cell(control_w_id)
    value_w_id = preprocessor.exec_code("lbl.model_id")
    value_w_id = preprocessor.eval_cell(value_w_id)
    control_w_ids = [control_w_id]

    matrix = preprocessor.get_static_values_by_widget(
        value_w_id, control_w_ids
    )
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
    ans = [
        '()',
        "('a',)",
        "('b',)",
        "('c',)",
        "('a', 'b')",
        "('a', 'c')",
        "('b', 'c')",
        "('a', 'b', 'c')",
    ]
    assert list(matrix.values()) == ans
