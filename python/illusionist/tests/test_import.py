import os

import illusionist
from illusionist.config import settings


def test_import():
    assert illusionist.__version__ is not None
    assert illusionist.__version__ != "0.0.0"
    assert len(illusionist.__version__) > 0


def test_assets_included():
    template = os.path.join(settings.templates_dir, "illusionist")
    assets = os.path.join(template, "assets")

    assert os.path.exists(os.path.join(template, "conf.json"))
    assert os.path.exists(os.path.join(template, "index.html.j2"))
    assert os.path.exists(os.path.join(assets, "illusionist-embed.css"))
    assert os.path.exists(os.path.join(assets, "illusionist-embed.css.map"))
    assert os.path.exists(os.path.join(assets, "illusionist-embed.js"))
    assert os.path.exists(os.path.join(assets, "illusionist-embed.js.map"))
