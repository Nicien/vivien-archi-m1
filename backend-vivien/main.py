from typing import List
from pydantic.dataclasses import dataclass
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_methods=["*"],
    # allow_headers=["*"],
)


@dataclass
class CellContent:
    playerName: str | None = None

@dataclass
class Grid:
    width: int
    height: int
    cells: List[CellContent]


@app.get("/grid")
async def read_grid() -> Grid:
    playersA = CellContent(playerName="Player A")
    return Grid(width=3, height=3, cells=[playersA, *[CellContent() for _ in range(8)]])


@app.get("/")
def read_root():
    return {"Hello": "Toto"}
