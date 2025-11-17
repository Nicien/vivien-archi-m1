from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/raphael")
async def raph():
    return {"error": 404, "message": "not found"}


class Cells:
    playersId: str
    player: str

class Grid:
     C
     

connected_clients=[]

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)

    
    try:
            while True:
                data = await websocket.receive_text()
                print(f"Message reçu : {data}")

                for client in connected_clients:
                    await client.send_text(f"Message: {data}")
    except WebSocketDisconnect:
            connected_clients.remove(websocket)
            print("Client déconnecté")