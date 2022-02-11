from abc import abstractmethod
from typing import Any, Protocol, Tuple, Type, TypeVar, runtime_checkable


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


@runtime_checkable
class ISeagullsApplicationPluginRegistrant(Protocol[ApplicationType]):

    @staticmethod
    @abstractmethod
    def register_plugins(application: ApplicationType) -> None:
        """
        Called at the start of the process for plugin devs to register their plugins in the app.
        """


class ILocatePluginRegistrants(Protocol):
    @abstractmethod
    def entry_points(
            self, group: str) -> Tuple[Type[ISeagullsApplicationPluginRegistrant], ...]: ...


class ISeagullsPluginClient(Protocol):

    @abstractmethod
    def register_plugins(self, application: ApplicationType) -> None:
        """
        Find all plugins and let them register plugins to the running application.
        """


class EntryPointsCallback(Protocol):
    def __call__(self, group: str) -> Tuple[Any]: ...
