from seagulls.app import (
    ApplicationType,
    PluginType,
    ISeagullsApplicationPlugin,
    IPluggableSeagullsApplication,
    ISeagullsPluginClient,
    ISeagullsApplicationPluginRegistrant,
)


def test_basics() -> None:
    # We just need to assert that our interfaces exists, and we are able to import them.
    assert ApplicationType
    assert PluginType
    assert ISeagullsApplicationPlugin
    assert IPluggableSeagullsApplication
    assert ISeagullsPluginClient
    assert ISeagullsApplicationPluginRegistrant
