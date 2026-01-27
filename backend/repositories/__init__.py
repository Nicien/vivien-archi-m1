from .grid_repository import GridRepository


class Repositories:
    grid_repository: GridRepository

    def __init__(self) -> None:
        self.grid_repository = GridRepository()
