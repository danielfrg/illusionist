import pytest
import ipywidgets
from illusionist import kernel_utils as ku


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
