from ._app_interfaces import ISeagullsApplication
from ._plugin_client import SeagullsEntryPointsPluginsClient, SeagullsEntryPointsPluginSource
from ._plugin_exceptions import DuplicatePluginError
from ._plugin_interfaces import (
    ApplicationType,
    IPluggableSeagullsApplication,
    ISeagullsApplicationPlugin,
    ISeagullsApplicationPluginRegistrant,
    ISeagullsPluginClient,
    PluginType
)

__all__ = [
    # App
    "ISeagullsApplication",
    # Plugin Client
    "SeagullsEntryPointsPluginsClient",
    "SeagullsEntryPointsPluginSource",
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
