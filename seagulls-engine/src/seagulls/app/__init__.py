from ._app_interfaces import ISeagullsApplication
from ._plugin_client import SeagullsEntryPointsPluginsClient
from ._plugin_interfaces import (
    ApplicationType,
    PluginType,
    ISeagullsApplicationPlugin,
    IPluggableSeagullsApplication,
    ISeagullsPluginClient,
    ISeagullsApplicationPluginRegistrant,
)
from ._plugin_exceptions import DuplicatePluginError

__all__ = [
    # App
    "ISeagullsApplication",
    # Plugin Client
    "SeagullsEntryPointsPluginsClient",
    # App Plugins
    "ApplicationType",
    "PluginType",
    "ISeagullsApplicationPlugin",
    "IPluggableSeagullsApplication",
    "ISeagullsPluginClient",
    "ISeagullsApplicationPluginRegistrant",
    # Exceptions
    "DuplicatePluginError",
]
