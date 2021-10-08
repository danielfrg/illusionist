import ipywidgets as W
import pytest

import illusionist.widgets as IW


@pytest.mark.parametrize("preprocessor", ["pandas.ipynb"], indirect=True)
def test_examples_pandas(preprocessor):
    """
    Verify that each output widget is affected by only one slider
    """
    onchange = preprocessor.widget_onchange_state
    # assert len(onchange["all_widgets"]) == 4
    assert len(onchange["onchange"]) == 2
    for value_w, values in onchange["onchange"].items():
        assert len(values["affected_by"]) == 1

