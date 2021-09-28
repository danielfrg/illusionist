import ipywidgets as W
import pytest

import illusionist.widgets as IW
from illusionist.preprocessor import hash_fn_plain


@pytest.mark.parametrize("class_", IW.NUMERIC_SINGLEVALUE_CONTROL_WIDGETS)
def test_hash_fn_plain_num_single_widget(class_):
    w = class_(min=1, max=5)
    w_states = [w.get_state() for w in [w]]
    assert hash_fn_plain(w_states) == "1"

    w.value = 5
    w_states = [w.get_state() for w in [w]]
    assert hash_fn_plain(w_states) == "5"


@pytest.mark.parametrize("class_", IW.NUMERIC_SINGLEVALUE_CONTROL_WIDGETS)
def test_hash_fn_plain_num_multiple_widgets(class_):
    w1 = class_(min=1, max=5)
    w2 = class_(min=6, max=10)
    w_states = [w.get_state() for w in [w1, w2]]
    assert hash_fn_plain(w_states) == "1,6"

    w1.value = 5
    w2.value = 8
    w_states = [w.get_state() for w in [w1, w2]]
    assert hash_fn_plain(w_states) == "5,8"


@pytest.mark.parametrize("class_", IW.NUMERIC_MULTIVALUE_CONTROL_WIDGETS)
def test_hash_fn_plain_num_multivalue_single(class_):
    w = class_(min=1, max=7, value=(2, 4))
    w_states = [w.get_state() for w in [w]]
    assert hash_fn_plain(w_states) == '"[2,4]"'

    w.value = (4, 7)
    w_states = [w.get_state() for w in [w]]
    assert hash_fn_plain(w_states) == '"[4,7]"'


@pytest.mark.parametrize("class_", IW.NUMERIC_MULTIVALUE_CONTROL_WIDGETS)
def test_hash_fn_plain_num_multivalue_multiple(class_):
    w1 = class_(min=1, max=7, value=(2, 4))
    w2 = class_(min=1, max=7, value=(1, 2))
    w_states = [w.get_state() for w in [w1, w2]]
    assert hash_fn_plain(w_states) == '"[2,4]","[1,2]"'

    w1.value = (1, 2)
    w2.value = (5, 7)
    w_states = [w.get_state() for w in [w1, w2]]
    assert hash_fn_plain(w_states) == '"[1,2]","[5,7]"'


@pytest.mark.parametrize("class_", IW.BOOLEAN_CONTROL_WIDGETS)
def test_hash_fn_plain_bool_single(class_):
    w = class_()
    w_states = [w.get_state() for w in [w]]
    assert hash_fn_plain(w_states) == '"false"'

    w.value = True
    w_states = [w.get_state() for w in [w]]
    assert hash_fn_plain(w_states) == '"true"'


@pytest.mark.parametrize("class_", IW.BOOLEAN_CONTROL_WIDGETS)
def test_hash_fn_plain_bool_multiple(class_):
    w1 = class_()
    w2 = class_()
    w_states = [w.get_state() for w in [w1, w2]]
    assert hash_fn_plain(w_states) == '"false","false"'

    w1.value = True
    w_states = [w.get_state() for w in [w1, w2]]
    assert hash_fn_plain(w_states) == '"true","false"'

    w2.value = True
    w_states = [w.get_state() for w in [w1, w2]]
    assert hash_fn_plain(w_states) == '"true","true"'


@pytest.mark.parametrize("class_", IW.SELECTION_SINGLEVALUE_CONTROL_WIDGETS)
def test_hash_fn_plain_selection_singlevalue(class_):
    options = ["a", "b", "c"]
    w = class_(options=options)
    w_states = [w.get_state() for w in [w]]
    assert hash_fn_plain(w_states) == "0"

    w.value = "b"
    w_states = [w.get_state() for w in [w]]
    assert hash_fn_plain(w_states) == "1"

    w.value = "c"
    w_states = [w.get_state() for w in [w]]
    assert hash_fn_plain(w_states) == "2"


@pytest.mark.parametrize("class_", [W.SelectionRangeSlider])
def test_hash_fn_plain_selection_multivalue_1(class_):
    options = ["a", "b", "c", "d"]
    w = class_(options=options)
    w_states = [w.get_state() for w in [w]]
    assert hash_fn_plain(w_states) == '"[0,0]"'

    w.value = ["a", "b"]
    w_states = [w.get_state() for w in [w]]
    assert hash_fn_plain(w_states) == '"[0,1]"'

    w.value = ["b", "c"]
    w_states = [w.get_state() for w in [w]]
    assert hash_fn_plain(w_states) == '"[1,2]"'

    w.value = ["a", "d"]
    w_states = [w.get_state() for w in [w]]
    assert hash_fn_plain(w_states) == '"[0,3]"'


@pytest.mark.parametrize("class_", [W.SelectMultiple])
def test_hash_fn_plain_selection_multivalue_2(class_):
    options = ["a", "b"]
    w = class_(options=options)
    w_states = [w.get_state() for w in [w]]
    assert hash_fn_plain(w_states) == '"[]"'

    w.value = ["a"]
    w_states = [w.get_state() for w in [w]]
    assert hash_fn_plain(w_states) == '"[0]"'

    w.value = ["b"]
    w_states = [w.get_state() for w in [w]]
    assert hash_fn_plain(w_states) == '"[1]"'

    w.value = ["a", "b"]
    w_states = [w.get_state() for w in [w]]
    assert hash_fn_plain(w_states) == '"[0,1]"'
