from dataclasses import dataclass
from repositories import Repositories
from .grid_service import GridService


@dataclass
class Services:
    repositories: Repositories

    def grid(self) -> GridService:
        return GridService(grid_repository=self.repositories.grid_repository)
