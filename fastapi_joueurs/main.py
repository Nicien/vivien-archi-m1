# from fastapi import FastAPI
# import uvicorn

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"message": "Hello, FastAPI!"}

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
from fastapi import FastAPI
from data import joueurs

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/joueurs")
def get_joueurs():
    # Convertir les dataclasses en dict pour JSON
    return [joueur.__dict__ for joueur in joueurs]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
