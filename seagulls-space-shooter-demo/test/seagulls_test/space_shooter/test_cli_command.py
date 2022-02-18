from seagulls.space_shooter._cli_command import GameCliCommand


class TestCliCommand:

    def test_basics(self):
        cli_command = GameCliCommand(
            "game_session",
            "active_scene_manager",
            "ship_selection_scene_factory",
            "space_shooter_scene"
        )

        cli_command.configure_parser("parser")
