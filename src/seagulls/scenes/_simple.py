import logging
from typing import List

from pygame import Surface
from seagulls.assets import AssetManager
from seagulls.pygame import GameScene
from seagulls.wizards import (
    SimpleWizard,
    SimpleWizardFactory,
)

logger = logging.getLogger(__name__)


class SimpleScene(GameScene):

    _asset_manager: AssetManager

    _wizards: List[SimpleWizard]

    _ticks: int

    def __init__(
            self,
            asset_manager: AssetManager,
            wizard_factory: SimpleWizardFactory):

        self._asset_manager = asset_manager
        self._wizard_factory = wizard_factory

        self._ticks = 0
        self._wizards = []

    def start(self) -> None:
        self._ticks = 0
        self._spawn_wizard()

    def update(self) -> None:
        self._ticks += 1
        if self._ticks % 100 == 0:
            self._spawn_wizard()
        for w in self._wizards:
            w.update()

    def render(self, surface: Surface) -> None:
        background = self._get_background()
        for w in self._wizards:
            w.render(background)

        surface.blit(background, (0, 0))

    def _spawn_wizard(self) -> None:
        self._wizards.append(self._wizard_factory.create())

    def _get_background(self) -> Surface:
        return self._asset_manager.load_sprite("environment/environment-sky")
