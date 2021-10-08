import os


import pytest


@pytest.fixture
def preprocessor(request):
    """
    A fixture to create an Illusionist.Preprocesor with an empty notebook
    """
    import nbformat

    from illusionist import preprocessor

    if hasattr(request, "param"):
        this_dir = os.path.abspath(os.path.dirname(__file__))
        examples_dir = os.path.join(this_dir, "..", "..", "..", "examples")
        nb_file = os.path.join(examples_dir, request.param)
        nb = nbformat.read(nb_file, as_version=4)
    else:
        nb = nbformat.v4.new_notebook()

    p = preprocessor.IllusionistPreprocessor(nb=nb)

    if hasattr(request, "param"):
        p.preprocess(nb, cleanup=False)
    else:
        p.execute(cleanup_kc=False)

        from illusionist import widgets
        from illusionist.utils import get_source

        p.exec_code(get_source(widgets))

    yield p

    p._cleanup_kernel()
