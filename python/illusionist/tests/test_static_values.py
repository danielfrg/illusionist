import ipywidgets as W
import pytest

import illusionist.widgets as IW


@pytest.mark.parametrize("class_", IW.NUMERIC_SINGLEVALUE_CONTROL_WIDGETS)
def test_static_values_num_nolink(preprocessor, class_):
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
    value_w_ids = [value_w_id]
    control_w_ids = [control_w_id]

    affected_by = preprocessor.get_affected_widgets(control_w_ids, value_w_ids)
    values = preprocessor.get_static_values(affected_by)

    # nothing link between the widgets
    assert len(values) == 0


@pytest.mark.parametrize("class_", IW.NUMERIC_SINGLEVALUE_CONTROL_WIDGETS)
def test_static_values_num_link(preprocessor, class_):
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
    value_w_ids = [value_w_id]
    control_w_ids = [control_w_id]

    affected_by = preprocessor.get_affected_widgets(control_w_ids, value_w_ids)
    values = preprocessor.get_static_values(affected_by)

    assert list(values.keys()) == value_w_ids
    assert list(values.values()) == [
        {
            "affected_by": control_w_ids,
            "values": {"-1": "-2", "-2": "-4", "-3": "-6", "0": "0"},
        }
    ]
