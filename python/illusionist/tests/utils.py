import pytest


@pytest.fixture
def preprocessor():
    import os
    import nbformat
    from illusionist import preprocessor

    # this_dir = os.path.abspath(os.path.dirname(__file__))
    # nb_file = os.path.join(this_dir, "widget-gallery.ipynb")

    nb = nbformat.v4.new_notebook()
    # cell = nbformat.v4.new_code_cell("import ipywidgets")
    # nb.cells.append(cell)
    # nb = nbformat.read(nb_file, as_version=4)
    # print(nb)
    # p = preprocessor.IllusionistPreprocessor()
    p = preprocessor.IllusionistPreprocessor(nb=nb)

    p.execute(cleanup_kc=False)

    from illusionist.utils import get_source
    from illusionist import widgets

    p.run_code(get_source(widgets))

    yield p

    p._cleanup_kernel()
