# costume_exceptions

class WrongFieldSize(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class WrongContentInput(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class WrongCellValue(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
