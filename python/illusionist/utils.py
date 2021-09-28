import inspect


def get_source(code):
    """
    Return the source code for a module or function
    """
    return inspect.getsource(code)
