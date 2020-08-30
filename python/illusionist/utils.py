import os
import pkg_resources
from pip._internal.utils.misc import dist_is_editable

distributions = {v.key: v for v in pkg_resources.working_set}
DEV_MODE = dist_is_editable(distributions["illusionist"])
_ = os.environ.get("ILLUSIONIST_DEV_MODE")
DEV_MODE = False if _ == "0" else DEV_MODE
# DEV_MODE = False
del distributions


def get_source(code):
    import inspect

    return inspect.getsource(code)
