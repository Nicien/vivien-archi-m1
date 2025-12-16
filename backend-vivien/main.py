from typing import List
from pydantic.dataclasses import dataclass
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@dataclass
class CellContent:
    selected: bool
    caption: str | None = None
    color: str  | None = None

@dataclass
class Grid:
    width: int
    height: int
    cells: List[CellContent]

GRID_SIZE = 10
grid = Grid(
    width=GRID_SIZE,
    height=GRID_SIZE,
    cells=[CellContent(selected=False) for _ in range(GRID_SIZE**2)]
)

grid.cells[0].color= 'white'

@app.get("/grid")
async def read_grid() -> Grid:
    return grid

@dataclass
class UpdateBody:
    caption: str
    color : str

@app.post("/cell/{cell_index}")
async def update_cell(cell_index: int, body: UpdateBody):
    if 0 <= cell_index < len(grid.cells):
        grid.cells[cell_index].caption = body.caption
        grid.cells[cell_index].selected = True
        grid.cells[cell_index].color = body.color
    return grid

