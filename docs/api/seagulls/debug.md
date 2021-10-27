## [seagulls](../seagulls).debug
Debug Tooling.

??? note "View Source"
    ```python
        """
        Debug Tooling.
        """
        from ._debug_hud import DebugHud

        __all__ = [
            "DebugHud",
        ]

    ```

### DebugHud

#### class `DebugHud` (seagulls.engine._game_object.GameObject):

??? note "View Source"
    ```python
        class DebugHud(GameObject):
            """
            UI Component to display FPS and other debug information during gameplay.
            """

            _game_clock: GameClock

            def __init__(self, game_clock: GameClock):
                """
                Initializes a Debug Hud where `game_clock` controls how we measure time.
                """
                self._game_clock = game_clock
                self._background = Surface((1024, 20))
                self._background.fill((100, 100, 100))
                self._background.set_alpha(100)
                self._font = Font(Path("assets/fonts/ubuntu-mono-v10-latin-regular.ttf"), 14)

            def tick(self) -> None:
                """
                Does nothing because Debug Huds do not need to perform any logic on tick().
                """
                pass

            def render(self, surface: Surface) -> None:
                """
                Renders the debug information onto the passed in Surface object.
                """
                fps = str(int(self._game_clock.get_fps())).rjust(3, " ")
                time = self._game_clock.get_time()
                img = self._font.render(
                    f"FPS: {fps} | MS: {time}",
                    True,
                    (20, 20, 20)
                )
                text_height = img.get_height()
                padding = (self._background.get_height() - text_height) / 2

                surface.blit(self._background, (0, 0))
                surface.blit(img, (10, padding))

    ```

UI Component to display FPS and other debug information during gameplay.



##### DebugHud(game_clock: seagulls.engine._game_clock.GameClock):

??? note "View Source"
    ```python
            def __init__(self, game_clock: GameClock):
                """
                Initializes a Debug Hud where `game_clock` controls how we measure time.
                """
                self._game_clock = game_clock
                self._background = Surface((1024, 20))
                self._background.fill((100, 100, 100))
                self._background.set_alpha(100)
                self._font = Font(Path("assets/fonts/ubuntu-mono-v10-latin-regular.ttf"), 14)

    ```

Initializes a Debug Hud where `game_clock` controls how we measure time.



##### def tick(self) -&gt; None:

??? note "View Source"
    ```python
            def tick(self) -> None:
                """
                Does nothing because Debug Huds do not need to perform any logic on tick().
                """
                pass

    ```

Does nothing because Debug Huds do not need to perform any logic on tick().



##### def render(self, surface: pygame.Surface) -&gt; None:

??? note "View Source"
    ```python
            def render(self, surface: Surface) -> None:
                """
                Renders the debug information onto the passed in Surface object.
                """
                fps = str(int(self._game_clock.get_fps())).rjust(3, " ")
                time = self._game_clock.get_time()
                img = self._font.render(
                    f"FPS: {fps} | MS: {time}",
                    True,
                    (20, 20, 20)
                )
                text_height = img.get_height()
                padding = (self._background.get_height() - text_height) / 2

                surface.blit(self._background, (0, 0))
                surface.blit(img, (10, padding))

    ```

Renders the debug information onto the passed in Surface object.
