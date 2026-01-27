from dataclasses import dataclass
import random
from uuid import uuid4
from ..repositories import GridRepository
from ..models import Grid, Player

PLAYER_COLORS = ["red", "blue", "green", "yellow", "purple", "orange"]

@dataclass
class GridService:
    grid_repository: GridRepository

    # def move_player(self, player: str, grid) -> None:
    #     self.grid_repository.set_content(CellConent)

    def reset(self) -> Grid:
        grid = self.grid_repository.grid()
        for cell in grid.cells:
            cell.caption = None
            cell.color = None
            cell.player = None
        return grid
    
    def add_player(self) -> str:
        grid = self.grid_repository.grid()
        # Place a new player at a random empty location in the grid
        empty_indices = [i for i, cell in enumerate(grid.cells) if cell.player is None]
        if empty_indices:
            raise ValueError("No empty space for a new player")
        player_position = random.choice(empty_indices)
        player = Player(id=str(uuid4()), color=random.choice(PLAYER_COLORS))
        grid.cells[player_position].player = player
        return player.id

    def remove_player(self, player_id: str) -> None:
        grid = self.grid_repository.grid()
        position = self.find_player_position(player_id)

        if position is not None:
            grid.cells[position].player = None

    # INSERT_YOUR_CODE
    # Find the position of the player in the grid
    def find_player_position(self, player_id: str) -> int | None:
        grid = self.grid_repository.grid()
        for idx, cell in enumerate(grid.cells):
            if cell.player is not None and cell.player.id == player_id:
                return idx
        return None
        