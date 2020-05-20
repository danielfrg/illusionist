import os

ROOT = os.path.dirname(__file__)
DEV_MODE = os.path.exists(os.path.join(ROOT, "../setup.py")) and os.path.exists(
    os.path.join(ROOT, "../share")
)
