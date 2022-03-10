from seagulls.space_shooter._shooter_scene_client import (
    ShooterSceneState,
    ShooterSceneStateClient
)


class TestShooterSceneStateClient:
    def test_basics(self) -> None:
        client = ShooterSceneStateClient()

        assert client.get_state() == ShooterSceneState.RUNNING

        client.update_state(ShooterSceneState.WON)

        assert client.get_state() == ShooterSceneState.WON
