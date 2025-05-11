class NotFoundError(Exception):
    """ Ошибка, когда объект не найден """
    def __init__(self, entity_name: str, entity_id: int):
        self.message = f"{entity_name} с id {entity_id} не найден"
        super().__init__(self.message)

class ConflictError(Exception):
    """ Ошибка, когда объект уже существует или конфликтует """
    def __init__(self, entity_name: str):
        self.message = f"{entity_name} уже существует"
        super().__init__(self.message)

class DatabaseError(Exception):
    """ Общая ошибка базы данных """
    def __init__(self, message: str = "Ошибка базы данных"):
        self.message = message
        super().__init__(self.message)