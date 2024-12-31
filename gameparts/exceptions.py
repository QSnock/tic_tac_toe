class CellOccupiedError(Exception):
    def __init__(
        self, message='Попытка изменить занятую ячейку'
    ):

        super().__init__(message)
