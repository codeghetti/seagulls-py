from ._game_scene import IGameScene


class EmptyScene(IGameScene):

    def start(self) -> None:
        raise RuntimeError("You're not supposed to start me.")

    def should_quit(self) -> bool:
        raise RuntimeError("You're not supposed to give me up. Ever.")

    def tick(self) -> None:
        raise RuntimeError("You're not supposed to tick me.")
