from pydantic.dataclasses import dataclass
from typing import List
from .player import Player

@dataclass
class CellContent:
    caption: str | None = None
    color: str  | None = None
    player: Player | None = None

@dataclass
class Grid:
    width: int
    height: int
    cells: List[CellContent]
