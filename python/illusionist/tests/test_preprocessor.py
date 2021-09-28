import ipywidgets
import pytest


# def test_pb(preprocessor):
# # def test_pb(preprocessor):
#     # preprocessor.exec_code("import ipywidgets")
#     # preprocessor.exec_code("w = ipywidgets.IntSlider(min=5, max=10)")
#     # w_id = preprocessor.eval_code("w.model_id")

#     w = ipywidgets.IntSlider(min=5, max=10)
#     w_state = w.get_state()
#     # w_id = list(preprocessor.widget_state.keys())[0]
#     assert possible_values(w_state)
#     # print(preprocessor.widget_state)

#     preprocessor._cleanup_kernel()
