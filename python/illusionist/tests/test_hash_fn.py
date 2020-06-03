import pytest

from illusionist.preprocessor import hash_fn
from illusionist.widgets import *  # noqa

from .utils import preprocessor


@pytest.mark.parametrize("class_", [IntSlider, BoundedIntText])
def test_hash_fn_int_single_value(class_):
    w = class_(min=1, max=5)
    w_states = [w.get_state() for w in [w]]
    assert hash_fn(w_states) == "1"

    w.value = 5
    w_states = [w.get_state() for w in [w]]
    assert hash_fn(w_states) == "5"


@pytest.mark.parametrize("class_", [IntSlider, BoundedIntText])
def test_hash_fn_int_multiple_single_value(class_):
    w1 = class_(min=1, max=5)
    w2 = class_(min=6, max=10)
    w_states = [w.get_state() for w in [w1, w2]]
    assert hash_fn(w_states) == "1,6"

    w1.value = 5
    w2.value = 8
    w_states = [w.get_state() for w in [w1, w2]]
    assert hash_fn(w_states) == "5,8"


@pytest.mark.parametrize("class_", BOOLEAN_CONTROL_WIDGETS)
def test_hash_fn_boolean(class_):
    w = class_()
    w_states = [w.get_state() for w in [w]]
    assert hash_fn(w_states) == '"false"'

    w.value = True
    w_states = [w.get_state() for w in [w]]
    assert hash_fn(w_states) == '"true"'


@pytest.mark.parametrize("class_", BOOLEAN_CONTROL_WIDGETS)
def test_hash_fn_boolean_multiple(class_):
    w1 = class_()
    w2 = class_()
    w_states = [w.get_state() for w in [w1, w2]]
    assert hash_fn(w_states) == '"false","false"'

    w1.value = True
    w_states = [w.get_state() for w in [w1, w2]]
    assert hash_fn(w_states) == '"true","false"'

    w2.value = True
    w_states = [w.get_state() for w in [w1, w2]]
    assert hash_fn(w_states) == '"true","true"'


@pytest.mark.parametrize(
    "class_", [SelectMultiple],
)
def test_hash_fn_selection_multi_value(class_):
    options = ["a", "b"]
    w = class_(options=options)
    w_states = [w.get_state() for w in [w]]
    assert hash_fn(w_states) == '"[]"'

    w.value = ["a"]
    w_states = [w.get_state() for w in [w]]
    assert hash_fn(w_states) == '"[0]"'

    w.value = ["b"]
    w_states = [w.get_state() for w in [w]]
    assert hash_fn(w_states) == '"[1]"'

    w.value = ["a", "b"]
    w_states = [w.get_state() for w in [w]]
    assert hash_fn(w_states) == '"[0,1]"'
