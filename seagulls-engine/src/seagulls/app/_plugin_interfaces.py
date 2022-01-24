from abc import abstractmethod
from typing import Protocol, TypeVar, Type, runtime_checkable


class ISeagullsApplicationPlugin(Protocol):

    @abstractmethod
    def on_registration(self) -> None:
        """
        Called when the plugin is first registered with the application.
        """


PluginType = TypeVar("PluginType", bound=ISeagullsApplicationPlugin)


class IPluggableSeagullsApplication(Protocol):

    @abstractmethod
    def register_plugin(self, plugin: ISeagullsApplicationPlugin) -> None: ...

    @abstractmethod
    def get_plugin(self, plugin: Type[PluginType]) -> PluginType: ...


ApplicationType = TypeVar("ApplicationType", contravariant=True)


class ISeagullsPluginClient(Protocol):

    @abstractmethod
    def register_plugins(self, application: ApplicationType) -> None:
        """
        Find all plugins and let them register plugins to the running application.
        """


@runtime_checkable
class ISeagullsApplicationPluginRegistrant(Protocol[ApplicationType]):

    @staticmethod
    @abstractmethod
    def register_plugins(application: ApplicationType) -> None:
        """
        Called at the start of the process for plugin devs to register their plugins in the app.
        """
