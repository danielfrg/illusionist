import pytest
import ipywidgets
from illusionist import kernel_utils as ku


# This needs an actual kernel I think
def test_get_output_mpl_value():
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from IPython.display import display, clear_output

out = ipywidgets.Output()

A = 5
f = 2
ax = plt.axes()
t = np.arange(0.0, f, 0.01)
s = A + np.sin(np.pi * t)

ax.plot(t, s)

ax.set(
    xlabel="time (s)",
    ylabel="voltage (mV)",
    title="About as simple as it gets, folks",
)
ax.grid()

with out:
    display(ax.figure)

outputs = out.outputs
# assert len(outputs) == 1
# assert outputs[0]["output_type"] == "display_data"
# assert "text/plain" in outputs[0]["data"]
# assert "text/png" in outputs[0]["data"]
