import logging
from typing import List

from seagulls.assets import AssetManager
from seagulls.pygame import (
    GameScene,
    Surface,
)
from seagulls.ui import DebugHud
from seagulls.wizards import (
    SimpleWizard,
    SimpleWizardFactory,
)

logger = logging.getLogger(__name__)


class SimpleScene(GameScene):

    _asset_manager: AssetManager
    _wizard_factory: SimpleWizardFactory
    _debug_hud: DebugHud

    _wizards: List[SimpleWizard]

    _ticks: int

    def __init__(
            self,
            asset_manager: AssetManager,
            wizard_factory: SimpleWizardFactory,
            debug_hud: DebugHud):

        self._asset_manager = asset_manager
        self._wizard_factory = wizard_factory
        self._debug_hud = debug_hud

        self._ticks = 0
        self._wizards = []

    def start(self) -> None:
        self._ticks = 0
        self._spawn_wizard()

    def update(self) -> None:
        self._ticks += 1
        # Occasionally spawn a new wizard unless we have 5 or more.
        if self._ticks % 100 == 0 and len(self._wizards) < 5:
            self._spawn_wizard()

        for w in self._wizards:
            w.update()

        self._debug_hud.update()

    def render(self, surface: Surface) -> None:
        background = self._get_background()
        for w in self._wizards:
            w.render(background)

        self._debug_hud.render(background)

        surface.blit(background, (0, 0))

    def _spawn_wizard(self) -> None:
        self._wizards.append(self._wizard_factory.create())

    def _get_background(self) -> Surface:
        return self._asset_manager.load_sprite("environment/environment-sky")
