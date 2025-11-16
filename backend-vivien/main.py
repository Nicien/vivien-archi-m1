from typing import List
from pydantic.dataclasses import dataclass
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
)

@dataclass
class CellContent:
    playerName: str | None = None
    is_rock: bool = False

@dataclass
class Grid:
    width: int
    height: int
    cells: List[CellContent]

# --- Grille stockée en mémoire (important pour /move !) ---
grid = Grid(
    width=3,
    height=3,
    cells=[
        CellContent(playerName="Player A"),
        CellContent(is_rock=True),
        CellContent(),
        CellContent(),
        CellContent(),
        CellContent(),
        CellContent(),
        CellContent(is_rock=True),
        CellContent(),
    ]
)

@app.get("/grid")
async def read_grid() -> Grid:
    return grid

# ----------- ÉTAPE 3 : route POST /move -------------
@app.post("/move")
async def move_player(request: Request):
    data = await request.json()
    direction = data.get("direction")

    # trouve l'index du joueur
    index = next(i for i, c in enumerate(grid.cells) if c.playerName)

    width = grid.width
    new_index = index

    if direction == "right":
        new_index = index + 1
    elif direction == "left":
        new_index = index - 1
    elif direction == "up":
        new_index = index - width
    elif direction == "down":
        new_index = index + width

    # limite du tableau
    if not (0 <= new_index < len(grid.cells)):
        return {"status": "blocked"}

    # vérifie le rocher
    if grid.cells[new_index].is_rock:
        return {"status": "rock"}

    # fait le mouvement
    grid.cells[new_index].playerName = grid.cells[index].playerName
    grid.cells[index].playerName = None

    return {"status": "ok", "grid": grid}

@app.get("/")
def read_root():
    return {"Hello": "Toto"}

