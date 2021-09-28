import pytest


@pytest.fixture
def preprocessor():
    """
    A fixture to create an Illusionist.Preprocesor with an empty notebook
    """
    import nbformat

    from illusionist import preprocessor

    nb = nbformat.v4.new_notebook()
    p = preprocessor.IllusionistPreprocessor(nb=nb)

    # this_dir = os.path.abspath(os.path.dirname(__file__))
    # nb_file = os.path.join(this_dir, "widget-gallery.ipynb")

    # cell = nbformat.v4.new_code_cell("import ipywidgets")
    # nb.cells.append(cell)
    # nb = nbformat.read(nb_file, as_version=4)
    # print(nb)
    # p = preprocessor.IllusionistPreprocessor()

    p.execute(cleanup_kc=False)

    from illusionist import widgets
    from illusionist.utils import get_source

    p.exec_code(get_source(widgets))

    yield p

    p._cleanup_kernel()
