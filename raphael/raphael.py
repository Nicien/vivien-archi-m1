from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/raphael")
async def raph():
    return {"error": 404, "message": "not found"}
