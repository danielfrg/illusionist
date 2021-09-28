def test_target_widgets(preprocessor):
    preprocessor.exec_code("w = W.IntSlider(min=0, max=3)")
    preprocessor.exec_code("lbl = W.Label()")

    value_w, control_w = preprocessor.get_target_widgets()
    assert len(value_w) == 2
    assert len(control_w) == 1
