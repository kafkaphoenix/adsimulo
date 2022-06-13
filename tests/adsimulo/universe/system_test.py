def test_instance(system, planet, star):
    assert star.name in system.stars
    assert planet.name in system.planets
