from pygame.surface import Surface
from typing import cast

from core.constants import CellValue
from core.state import World, Unit
from .LayerComponent import LayerComponent
from ...theme.Theme import Theme


class UnitsComponent(LayerComponent):
    def __init__(self, theme: Theme, world: World):
        super().__init__(theme, world.units, "units")
        self.__units = world.units

    def render(self, surface: Surface):
        super().render(surface)
        tileset = self.tileset.surface
        tilesRects = self.tileset.getTilesRects()

        renderer = self.createRenderer(surface)
        cellsSlice = renderer.cellsSlice
        cells = self.__units.cells[cellsSlice]

        valid = cells == CellValue.UNITS_UNIT
        for dest, _, item, _ in renderer.items(valid):
            unit = cast(Unit, item)
            rects = tilesRects[unit.unitClass]
            surface.blit(tileset, dest, rects[unit.playerId])

