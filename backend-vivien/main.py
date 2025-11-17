from typing import List
from pydantic.dataclasses import dataclass
from fastapi import FastAPI, Body
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
    playerName: str | None = None

@dataclass
class Grid:
    width: int
    height: int
    cells: List[CellContent]

grid = Grid(
    width=3,
    height=3,
    cells=[CellContent() for _ in range(9)]
)

@app.get("/grid")
async def read_grid() -> Grid:
    return grid  

@app.post("/cell/{cell_index}")
async def update_cell(cell_index: int, body: dict = Body(...)):
    if 0 <= cell_index < len(grid.cells):
        grid.cells[cell_index].playerName = body.get("playerName")
    return grid
