from abc import abstractmethod

from typing import Protocol, Iterable, Tuple

from dataclasses import dataclass

from argparse import ArgumentParser
from seagulls.cli import ICliCommand


class IExecutable(Protocol):
    @abstractmethod
    def execute(self) -> None:
        pass


class ITick(Protocol):
    @abstractmethod
    def tick(self) -> None:
        pass


class GameSessionStages:

    _stages: Tuple[IExecutable, ...]

    def stages(self) -> Iterable[IExecutable]:
        return self._stages


class GameSession:

    _session_stages: GameSessionStages

    def run(self) -> None:
        for stage in self._session_stages.stages():
            stage.execute()


@dataclass()
class SessionBuilderConfig:
    scene: ITick


class GameSessionBuilder:
    _config: SessionBuilderConfig

    def scene(self, scene: ITick) -> None:
        self._config.scene = scene

    def build(self) -> GameSession:
        return GameSession()


class GameCliCommand(ICliCommand):

    def configure_parser(self, parser: ArgumentParser) -> None:
        pass

    def execute(self) -> None:
        builder = GameSessionBuilder()
        builder.build().run()

        session_state_client = GameSessionStateClient()
        session_window_client = GameSessionWindowClient()
        game_input_client = GameInputClient(session_state_client=session_state_client)
        scene = MainScene(
            game_input_client=game_input_client,
            session_window_client=session_window_client,
            asset_manager=self._asset_manager,
        )

        process_input = executable(game_input_client.process_input)
        update_scene = executable(scene.update)
        render_scene = executable(scene.render)

        session_frame_client = GameSessionFrameClient(
            session_state_client=session_state_client,
            frame_stages=tuple([
                process_input,
                update_scene,
                render_scene,
            ]),
        )

        initialize = InitializeGameSessionCommand(
            session_state_client=session_state_client,
            session_window_client=session_window_client,
        )
        run_game_loop = RunGameLoopCommand(session_frame_client=session_frame_client)
        shutdown = ShutdownGameSessionCommand(
            session_state_client=session_state_client,
            session_window_client=session_window_client,
        )

        session = GameSessionClient(session_stages=tuple([initialize, run_game_loop, shutdown]))

        session.run()
