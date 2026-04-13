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
    is_exit: bool = False

@dataclass
class Grid:
    width: int
    height: int
    cells: List[CellContent]
    collisions: int = 0
    level: int = 1

def create_level(level_num: int) -> Grid:
    cells = [CellContent() for _ in range(25)] # Grille 5x5
    
    if level_num == 1:
        # Labyrinthe Niveau 1 (Chemin validé et jouable)
        rock_indices = [2, 6, 11, 12, 14, 18, 20, 21]
        for i in rock_indices: cells[i].is_rock = True
        
        cells[0].playerName = "Player A" # Départ Joueur A
        cells[4].playerName = "Player B" # Départ Joueur B
        cells[24].is_exit = True         # Sortie (Fin)
        return Grid(width=5, height=5, cells=cells, level=1)
        
    else:
        # Labyrinthe Niveau 2
        rock_indices = [3, 5, 6, 8, 13, 16, 17, 18]
        for i in rock_indices: cells[i].is_rock = True
        
        cells[0].playerName = "Player A"
        cells[1].playerName = "Player B"
        cells[24].is_exit = True
        return Grid(width=5, height=5, cells=cells, level=2)

grid = create_level(1)

@app.get("/grid")
async def read_grid() -> Grid:
    return grid

@app.post("/reset")
async def reset_grid(request: Request):
    global grid
    data = await request.json()
    target_level = data.get("level", 1)
    
    if target_level > 2:
        target_level = 1 # Si on a fini tous les niveaux, on boucle
        
    grid = create_level(target_level)
    return {"status": "ok", "grid": grid}

@app.post("/move")
async def move_player(request: Request):
    global grid
    data = await request.json()
    direction = data.get("direction")
    player_to_move = data.get("playerName", "Player A")

    try:
        index = next(i for i, c in enumerate(grid.cells) if c.playerName == player_to_move)
    except StopIteration:
        return {"status": "error"}

    width = grid.width
    new_index = index

    # Logique de déplacement avec blocage des bords
    if direction == "right":
        if index % width == width - 1:
            grid.collisions += 1
            return {"status": "blocked", "grid": grid}
        new_index = index + 1
    elif direction == "left":
        if index % width == 0:
            grid.collisions += 1
            return {"status": "blocked", "grid": grid}
        new_index = index - 1
    elif direction == "up":
        new_index = index - width
    elif direction == "down":
        new_index = index + width

    # Limites haut/bas
    if not (0 <= new_index < len(grid.cells)):
        grid.collisions += 1
        return {"status": "blocked", "grid": grid}

    # Roches
    if grid.cells[new_index].is_rock:
        grid.collisions += 1
        return {"status": "rock", "grid": grid}
        
    # Collision avec l'autre joueur
    if grid.cells[new_index].playerName is not None:
        grid.collisions += 1
        return {"status": "player_crash", "grid": grid}

    # Fait le mouvement
    grid.cells[new_index].playerName = grid.cells[index].playerName
    grid.cells[index].playerName = None

    # Victoire si le joueur arrive sur la case de sortie
    if grid.cells[new_index].is_exit:
        return {"status": "win", "grid": grid}

    return {"status": "ok", "grid": grid}