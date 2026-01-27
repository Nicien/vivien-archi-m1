from pydantic.dataclasses import dataclass
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from dataclasses import asdict  # Pour convertir la grille en JSON

from backend.repositories import Repositories
from backend.models import Grid
from backend.services import Services


repositories = Repositories()
services = Services(repositories)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

active_clients: List[WebSocket] = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_clients.append(websocket)

    grid_service = services.grid()

    player_id = grid_service.add_player()

    try:
        # Send the updated grid (including the new player) to everyone
        await broadcast_grid()
        
        while True:
            await websocket.receive_text()
            
    except WebSocketDisconnect:
        active_clients.remove(websocket)

        grid_service.remove_player(player_id)
        await broadcast_grid()

async def broadcast_grid():
    grid = repositories.grid_repository.grid()
    grid_dict = asdict(grid)
    for client in active_clients:
        await client.send_json(grid_dict)

@app.get("/grid")
async def read_grid() -> Grid:
    grid = repositories.grid_repository.grid()
    return grid

@dataclass
class UpdateBody:
    caption: str
    color : str

@app.post("/cell/{cell_index}")
async def update_cell(cell_index: int, body: UpdateBody):
    grid = repositories.grid_repository.grid()
    if 0 <= cell_index < len(grid.cells):
        grid.cells[cell_index].caption = body.caption
        grid.cells[cell_index].color = body.color
        
        await broadcast_grid()
        
    return grid

@app.post("/reset")
async def reset_grid():
    grid = services.grid().reset()
    await broadcast_grid()
    return grid
