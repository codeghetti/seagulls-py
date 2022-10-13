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
from ._dishes_client import Dish, DishesClient
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
                # Fakes
                Country(name="japan", position=Position(1700, 430)),
                Country(name="senegal", position=Position(852, 567)),
                Country(name="south africa", position=Position(1065, 835)),
            ])),
            dishes_client=DishesClient(tuple([
                Dish(
                    name="Bon O Bon",
                    description=[
                        "These delicious chocolate covered bon bons",
                        "contain a smooth and rich peanut cream filling.",
                        "The Bon O Bon is one of the most famous brands",
                        "of the Arcor company in… Argentina!",
                        "",
                        "",
                        "",
                        "  — World Traveler, Fitz",
                    ],
                    country="argentina",
                ),
                Dish(
                    name="Zacuscă",
                    description=[
                        "This roasted eggplant and pepper spread is",
                        "the perfect snack or appetizer! Although",
                        "similar spreads are found in many countries",
                        "in the Balkan region, the Zacuscă is most",
                        "popular in… Romania!",
                        "",
                        "",
                        "  — World Traveler, Fitz",
                    ],
                    country="romania",
                ),
                Dish(
                    name="Lilikoi Juice",
                    description=[
                        "The manufacturer of this drink first started",
                        "canning juice at the end of the 1950s. This",
                        "passion fruit juice and many others are made by",
                        "the Kurihara family in… Hawaii, USA!",
                        "",
                        "",
                        "",
                        "  — World Traveler, Fitz",
                    ],
                    country="united states",
                ),
                Dish(
                    name="Aero",
                    description=[
                        "Aero is an aerated chocolate bar manufactured by",
                        "Nestlé. Originally produced by Rowntree's, Aero",
                        "bars were introduced  as the \"new chocolate\" in",
                        "1935 to the… United Kingdom!",
                        "",
                        "",
                        "",
                        "  — World Traveler, Fitz",
                    ],
                    country="united kingdom",
                ),
                Dish(
                    name="Quesifritos",
                    description=[
                        "This snack is made from exctruded corn grits and",
                        "then fried and flavored with cheese! I couldn't",
                        "find any other details in a language I speak so",
                        "the rest of this dialog is completely made up!",
                        "These delicacies were first introduced in 1923 to",
                        "the people of… Guatemala!",
                        "",
                        "  — World Traveler, Fitz",
                    ],
                    country="guatemala",
                ),
                Dish(
                    name="Kopiko",
                    description=[
                        "Kopiko Coffee Candy is for coffee lovers that also",
                        "love to eat candy! If you love the flavor of",
                        "drinking coffee, but don't want to drink it, then",
                        "have some in a candy form! This delicious treat is",
                        "a popular indulgence in its country of origin…",
                        "Indonesia!",
                        "",
                        "  — World Traveler, Fitz",
                    ],
                    country="indonesia",
                ),
                Dish(
                    name="Vegemite",
                    description=[
                        "Vegemite is a thick, dark brown food spread made",
                        "from leftover brewers' yeast extract with various",
                        "vegetable and spice additives. Vegemite is salty,",
                        "slightly bitter, malty, and rich in glutamates –",
                        "giving it an umami flavour similar to beef",
                        "bouillon. Vegemite first appeared in 1923 in the",
                        "country of… Australia!",
                        "  — World Traveler, Fitz",
                    ],
                    country="australia",
                ),
                Dish(
                    name="Colombiana",
                    description=[
                        "Described by Wikipedia as \"a cola champagne\",",
                        "this fancy drink can be found in every household",
                        "of the country of… Colombia!",
                        "",
                        "",
                        "",
                        "",
                        "  — World Traveler, Fitz",
                    ],
                    country="colombia",
                ),
                Dish(
                    name="Kolo",
                    description=[
                        "Often enjoyed as a snack – after meals, along with",
                        "coffee or some bear; Kolo is an easy to make dish",
                        "most commonly found in… Ethiopia!",
                        "",
                        "",
                        "",
                        "",
                        "  — World Traveler, Fitz",
                    ],
                    country="ethiopia",
                ),
                Dish(
                    name="Hanuta",
                    description=[
                        "Hazelnut slices with roasted hazelnut pieces in",
                        "cocoa cream between two wafers. Hanuta brings",
                        "together the tastiest of the confectionery",
                        "department in one snack! Hanuta made its debut",
                        "in 1959 to the people of… Germany!",
                        "",
                        "",
                        "  — World Traveler, Fitz",
                    ],
                    country="germany",
                ),
                Dish(
                    name="Chanas",
                    description=[
                        "An amazing source of protein, fiber, folate,",
                        "minerals, and fatty acids; this snack is low",
                        "in fat and packed with energy! Dry roasted",
                        "chana, or chickpeas, are typically eaten as a",
                        "snack in… India!",
                        "",
                        "",
                        "  — World Traveler, Fitz",
                    ],
                    country="india",
                ),
                Dish(
                    name="Moretti Biscuits",
                    description=[
                        "Moretti al Pistachios are exquisite cookies",
                        "to be enjoyed at all times! The pastry, made",
                        "with top quality ingredients, enhances the",
                        "taste and sweetness of pistachio cream, all",
                        "embellished with a whole shelled pistachio.",
                        "These delicious treats are often enjoyed by",
                        "the people of… Italy!",
                        "  — World Traveler, Fitz",
                    ],
                    country="italy",
                ),
            ])),
            players=(
                "Player 1",
                "Player 2",
                "Player 3",
                "Player 4",
                "Player 5",
                "Player 6",
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
