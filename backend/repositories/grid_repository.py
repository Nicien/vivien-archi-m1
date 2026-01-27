from models import Grid, CellContent


GRID_SIZE = 10
global_grid = Grid(
    width=GRID_SIZE,
    height=GRID_SIZE,
    cells=[CellContent() for _ in range(GRID_SIZE**2)]
)
global_grid.cells[0].color= 'white'

class GridRepository:

    def grid(self) -> Grid:
        return global_grid
    
    # def set_content(self, position: int, content: CellContent):
    #     grid.cells[position] = content

    # def cell(self, position: int)-> CellContent:
    #     return grid.cells[position]
