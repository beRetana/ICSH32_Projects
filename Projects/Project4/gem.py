# gem.py

# Contains the class for gems

from costume_exceptions import *
from enum import Enum


class GemState(Enum):
    EMPTY = 0
    FALLER = 1
    FALLER_LANDED = 2
    FROZEN = 3
    MATCH = 4

class Gem:

    def __init__(self, color: str, state = GemState.EMPTY):
        self._color = color.upper()
        self._state = state

    def update_state(self, new_state: GemState)-> None:
        'Updates the state of the gem'

        self._state = new_state

    def get_state(self)-> GemState:
        'Returns the current state of the gem'

        return self._state

    def get_color(self)-> str:
        'Returns the current color of the gem'

        return self._color

    def set_color(self, new_color: str)->None:
        'Sets a new color to the gem'
        self._color = new_color

    def get_formated_state(self)-> str:
        'Returns a string fomated status of the gem'

        status_format = ""

        match self._state:
            case GemState.FALLER:
                status_format = f"[{self._color}]"
            case GemState.FALLER_LANDED:
                status_format = f"|{self._color}|"
            case GemState.FROZEN:
                status_format = f" {self._color} "
            case GemState.MATCH:
                status_format = f"*{self._color}*"

        return status_format

    def is_valid_color(self, color: str)-> bool:
        'Returns whether the value is a valid color for a gem'

        match color:
            case "S":
                return True
            case "T":
                return True
            case "V":
                return True
            case "W":
                return True
            case "X":
                return True
            case "Y":
                return True
            case "Z":
                return True
            
        return False
