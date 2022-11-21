from argparse import ArgumentParser

from ._game_session import GameSessionBuilder
from seagulls.cli import ICliCommand


class GameCliCommand(ICliCommand):

    def configure_parser(self, parser: ArgumentParser) -> None:
        pass

    def execute(self) -> None:
        builder = GameSessionBuilder()
        builder.build().run()
        #
        # session_state_client = GameSessionStateClient()
        # session_window_client = GameSessionWindowClient()
        # game_input_client = GameInputClient(session_state_client=session_state_client)
        # scene = MainScene(
        #     game_input_client=game_input_client,
        #     session_window_client=session_window_client,
        #     asset_manager=self._asset_manager,
        # )
        #
        # process_input = executable(game_input_client.process_input)
        # update_scene = executable(scene.update)
        # render_scene = executable(scene.render)
        #
        # session_frame_client = GameSessionFrameClient(
        #     session_state_client=session_state_client,
        #     frame_stages=tuple([
        #         process_input,
        #         update_scene,
        #         render_scene,
        #     ]),
        # )
        #
        # initialize = InitializeGameSessionCommand(
        #     session_state_client=session_state_client,
        #     session_window_client=session_window_client,
        # )
        # run_game_loop = RunGameLoopCommand(session_frame_client=session_frame_client)
        # shutdown = ShutdownGameSessionCommand(
        #     session_state_client=session_state_client,
        #     session_window_client=session_window_client,
        # )
        #
        # session = GameSessionClient(session_stages=tuple([initialize, run_game_loop, shutdown]))
        #
        # session.run()
