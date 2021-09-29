def test_affected_no_links(preprocessor):
    preprocessor.exec_code(
        """
w = W.IntSlider(min=0, max=3)
lbl = W.Label()
"""
    )

    _ = preprocessor.exec_code("w.model_id")
    w_id = preprocessor.eval_cell(_)
    _ = preprocessor.exec_code("lbl.model_id")
    lbl_id = preprocessor.eval_cell(_)

    value_w, control_w = preprocessor.get_target_widgets()
    links = preprocessor.get_affected_widgets(control_w, value_w)
    assert len(links) == 2
    assert w_id in links
    assert lbl_id in links
    for w_id, aff_by in links.items():
        assert len(aff_by) == 0


def test_affected_1_in_1_out(preprocessor):
    preprocessor.exec_code(
        """
slider = W.IntSlider(min=0, max=3)
lbl = W.Label()

def update(args):
    lbl.value = str(slider.value)

update(None)
slider.observe(update, "value")
"""
    )

    _ = preprocessor.exec_code("slider.model_id")
    slider_id = preprocessor.eval_cell(_)
    _ = preprocessor.exec_code("lbl.model_id")
    lbl_id = preprocessor.eval_cell(_)

    value_w, control_w = preprocessor.get_target_widgets()
    links = preprocessor.get_affected_widgets(control_w, value_w)
    assert len(links) == 2
    assert slider_id in links
    assert len(links[slider_id]) == 0
    assert len(links[lbl_id]) == 1


def test_affected_1_in_multi_out(preprocessor):
    preprocessor.exec_code(
        """
slider = W.IntSlider(min=0, max=3)
lbl = W.Label()
int = W.BoundedIntText(min=0, max=3)

def update(args):
    lbl.value = str(slider.value)
    int.value = slider.value

update(None)
slider.observe(update, "value")
"""
    )

    _ = preprocessor.exec_code("slider.model_id")
    slider_id = preprocessor.eval_cell(_)
    _ = preprocessor.exec_code("lbl.model_id")
    lbl_id = preprocessor.eval_cell(_)
    _ = preprocessor.exec_code("int.model_id")
    int_id = preprocessor.eval_cell(_)

    value_w, control_w = preprocessor.get_target_widgets()
    links = preprocessor.get_affected_widgets(control_w, value_w)
    assert len(links) == 3
    assert slider_id in links
    assert len(links[slider_id]) == 0
    assert len(links[lbl_id]) == 1
    assert len(links[int_id]) == 1


def test_affected_1_out_multi_in(preprocessor):
    preprocessor.exec_code(
        """
slider = W.IntSlider(min=0, max=3)
int = W.BoundedIntText(min=0, max=3)
lbl = W.Label()

def update(args):
    lbl.value = str(slider.value + int.value)

update(None)
slider.observe(update, "value")
int.observe(update, "value")
"""
    )

    _ = preprocessor.exec_code("slider.model_id")
    slider_id = preprocessor.eval_cell(_)
    _ = preprocessor.exec_code("lbl.model_id")
    lbl_id = preprocessor.eval_cell(_)
    _ = preprocessor.exec_code("int.model_id")
    int_id = preprocessor.eval_cell(_)

    value_w, control_w = preprocessor.get_target_widgets()
    links = preprocessor.get_affected_widgets(control_w, value_w)
    assert len(links) == 3
    assert slider_id in links
    assert len(links[slider_id]) == 0
    assert len(links[int_id]) == 0
    assert len(links[lbl_id]) == 2
