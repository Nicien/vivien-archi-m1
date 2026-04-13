import asyncio
import json
from pydantic.dataclasses import dataclass
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from dataclasses import asdict
from dataclasses import asdict, replace

from repositories import Repositories
from models import Grid
from services import Services

repositories = Repositories()
services = Services(repositories)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


is_playing = False          #variable de l'etat de la vidéo
saved_grid_state = None     #save de l'etat de la grille avant le lancement de la vidéo

# Chargement du dataset
try:
    with open("data.json", "r") as f:
        BAD_APPLE_DATA = json.load(f)
except Exception as e:
    BAD_APPLE_DATA = []
    print(f"Dataset non chargé : {e}")

active_clients: List[WebSocket] = []


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_clients.append(websocket)
    grid_service = services.grid()
    player_id = grid_service.add_player()
    try:
        await broadcast_grid()
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        if websocket in active_clients:
            active_clients.remove(websocket)
        grid_service.remove_player(player_id)
        await broadcast_grid()

async def broadcast_grid():
    grid = repositories.grid_repository.grid()
    grid_dict = asdict(grid)
    
    async def send_to_client(client):
        try:
            await client.send_json(grid_dict)
        except:
            if client in active_clients:
                active_clients.remove(client)
    
    await asyncio.gather(*[send_to_client(client) for client in list(active_clients)], return_exceptions=True)



@dataclass
class UpdateBody:
    caption: str
    color: str
    size: int = 10

@app.post("/cell/{cell_index}")
async def update_cell(cell_index: int, body: UpdateBody):
    grid = repositories.grid_repository.grid()
    if 0 <= cell_index < len(grid.cells):
        grid.cells[cell_index].caption = body.caption
        grid.cells[cell_index].color = body.color
        await broadcast_grid()
    return grid


@app.post("/play-bad-apple")
async def play_bad_apple():
    global is_playing, saved_grid_state
    
    if is_playing or not BAD_APPLE_DATA:
        return {"error": "Impossible de lancer"}
    
    grid = repositories.grid_repository.grid()
    
    #copie de l'état actuel de la Grid avant le lancement de la video
    saved_grid_state = {
        "width": grid.width,
        "height": grid.height,
        "cells": [replace(c) for c in grid.cells] 
    }
    
    is_playing = True #lancement
    CellClass = type(grid.cells[0])
    
    # Détection de la taille du dataset
    first_frame = BAD_APPLE_DATA[0]
    new_height = len(first_frame) # nombre de liste dans la premiere liste
    new_width = len(first_frame[0])
    
    grid.width = new_width
    grid.height = new_height
    grid.cells = [CellClass(caption="", color="#ffffff") for _ in range(grid.width * grid.height)]
    
    await broadcast_grid()
    await asyncio.sleep(0.5)

    for frame in BAD_APPLE_DATA:
        if not is_playing:
            break
        for r_idx, row in enumerate(frame):
            for c_idx, value in enumerate(row):
                idx = r_idx * new_width + c_idx
                if idx < len(grid.cells):
                    grid.cells[idx].color = "#000000" if value == 1 else "#ffffff"
        await broadcast_grid()
        await asyncio.sleep(0.04)
    
    is_playing = False
    return {"status": "Terminé"}

@app.post("/reset")
async def reset_grid():
    global is_playing, saved_grid_state
    is_playing = False # Arrête le clip si il tourne
    
    grid = repositories.grid_repository.grid()
    
    # --- RESTAURATION ---
    if saved_grid_state:
        grid.width = saved_grid_state["width"]
        grid.height = saved_grid_state["height"]
        grid.cells = saved_grid_state["cells"]
        saved_grid_state = None # On vide la sauvegarde après l'avoir utilisée
    else:
        # Si aucune sauvegarde, on fait un reset standard
        services.grid().reset()
        grid.width = 10
        grid.height = 10
        CellClass = type(grid.cells[0])
        grid.cells = [CellClass(caption="", color="transparent") for _ in range(100)]
    
    await broadcast_grid()
    return grid
