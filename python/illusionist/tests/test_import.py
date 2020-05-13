def test_import():
    import illusionist

    assert illusionist.__version__ is not None
    assert illusionist.__version__ != "0.0.0"
    assert len(illusionist.__version__) > 0
