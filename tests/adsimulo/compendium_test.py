def test_instance(compendium, system, civilisation):
    assert system.name in compendium.galaxy
    assert civilisation.name in compendium.civilisations
