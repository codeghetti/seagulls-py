import random
from argparse import ArgumentParser

from seagulls.assets import AssetManager
from seagulls.cli import ICliCommand
from ._executable import executable
from ._main import GameInputClient
from ._session_client import InitializeGameSessionCommand, RunGameLoopCommand, \
    ShutdownGameSessionCommand, GameSessionClient
from ._session_frame_client import GameSessionFrameClient
from ._session_state_client import GameSessionStateClient
from ._session_window_client import GameSessionWindowClient

from ._countries_client import CountriesClient, Country
from ._dishes_client import Dish, DishInput, DishesClient, GptDishesClient
from ._position import Position
from ._scene import MainScene
from ._shots_client import ShotsClient


class GameCliCommand(ICliCommand):

    _asset_manager: AssetManager

    def __init__(self, asset_manager: AssetManager) -> None:
        self._asset_manager = asset_manager

    def configure_parser(self, parser: ArgumentParser) -> None:
        pass

    def execute(self) -> None:
        session_state_client = GameSessionStateClient()
        session_window_client = GameSessionWindowClient()
        game_input_client = GameInputClient(session_state_client=session_state_client)

        dishes_input = [
            DishInput(country="argentina"),
            DishInput(country="australia"),
            DishInput(country="colombia"),
            DishInput(country="ethiopia"),
            DishInput(country="germany"),
            DishInput(country="guatemala"),
            DishInput(country="india"),
            DishInput(country="indonesia"),
            DishInput(country="italy"),
            DishInput(country="romania"),
            DishInput(country="united kingdom"),
            DishInput(country="united states"),
            DishInput(country="japan"),
            DishInput(country="senegal"),
            DishInput(country="south africa"),
        ]
        random.shuffle(dishes_input)

        scene = MainScene(
            game_input_client=game_input_client,
            session_window_client=session_window_client,
            asset_manager=self._asset_manager,
            shots_client=ShotsClient(),
            countries_client=CountriesClient(tuple([
                Country(name="argentina", position=Position(580, 840)),
                Country(name="australia", position=Position(1680, 800)),
                Country(name="colombia", position=Position(525, 630)),
                Country(name="ethiopia", position=Position(1145, 600)),
                Country(name="germany", position=Position(989, 329)),
                Country(name="guatemala", position=Position(433, 562)),
                Country(name="india", position=Position(1365, 510)),
                Country(name="indonesia", position=Position(1563, 659)),
                Country(name="italy", position=Position(999, 379)),
                Country(name="romania", position=Position(1070, 360)),
                Country(name="united kingdom", position=Position(926, 310)),
                Country(name="united states", position=Position(390, 420)),
                Country(name="japan", position=Position(1700, 430)),
                Country(name="senegal", position=Position(852, 567)),
                Country(name="south africa", position=Position(1065, 835)),
            ])),
            dishes_client=GptDishesClient(tuple(dishes_input[:5])),
            players=(
                "J",
                "T",
                "L",
                # "Player 3",
                # "Player 4",
                # "Player 5",
                # "Player 6",
            ),
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
