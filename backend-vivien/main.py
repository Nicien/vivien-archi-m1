from typing import List
from dataclasses import asdict # Pour convertir la grille en JSON
from pydantic.dataclasses import dataclass
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
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
    cells=[CellContent() for _ in range(GRID_SIZE**2)]
)
grid.cells[0].color= 'white'

active_clients: List[WebSocket] = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_clients.append(websocket) 
    try:
        await websocket.send_json(asdict(grid))
        
        while True:
            await websocket.receive_text()
            
    except WebSocketDisconnect:
        active_clients.remove(websocket)

async def broadcast_grid():
    grid_dict = asdict(grid)
    for client in active_clients:
        await client.send_json(grid_dict)

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
        grid.cells[cell_index].color = body.color
        
        await broadcast_grid()
        
    return grid
