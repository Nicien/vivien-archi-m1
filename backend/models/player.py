from pydantic.dataclasses import dataclass

@dataclass
class Player:
    id: str
    color: str
