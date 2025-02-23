from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, Union, Optional, Dict, Any

from core.constants import UnitClass
from core.logic import DistanceMap
from core.state import Unit

if TYPE_CHECKING:
    from ..Mouse import Mouse
    from ..mode.GameMode import GameMode


class IComponentListener:

    # World

    def worldCellClicked(self, cell: Tuple[int, int], mouse: Mouse):
        pass

    def worldCellEntered(self, cell: Tuple[int, int], mouse: Mouse, dragging: bool):
        pass

    def viewChanged(self, view: Tuple[int, int]):
        pass

    # Edition

    def mainBrushSelected(self, layerName: str, values: Dict[str, Any]):
        pass

    def secondaryBrushSelected(self, layerName: str, values: Dict[str, Any]):
        pass

