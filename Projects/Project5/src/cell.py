# cell.y

# Handles the logic for the class Cell

from costume_exceptions import *
from enum import Enum
from gem import Gem, GemState
from collections import namedtuple

# Cell object is to manage the grid with objects always in them
# it will be easier to have the cell manage it's content and access
# the cell rather than than checking for a gem or empty space.

EMPTY = "   "
Location = namedtuple("Location", ["row", "column"])
class Cell:

    def __init__(self, location: Location):
        self._content = EMPTY
        self._location = location

    def get_location(self)-> Location:
        'Returns the location of the cell'
        location = Location(self._location.row, self._location.column)
        return location

    def set_location(self, location: Location)-> None:
        "Changes the location of the cell"
        self._location = Location(location.row, location.column)

    def add_content(self, gem: Gem)-> None:
        'Adds a gem to the cell'

        if not self.contains_gem():
            self._content = gem

    def pop_content(self, new_content = EMPTY)-> str|Gem:
        'Replaces the content in the cell and returns it'

        content = self._content
        self._content = new_content
        return content

    def peek_content(self)-> str|Gem:
        'Returns a copy of the content in the cell'

        content = self._content
        return self._content

    def get_formated_content(self)-> str:
        'Returns the formates state of gem is any in there or empty state'
        
        if self.contains_gem():
            return self._content.get_formated_state()

        return EMPTY
        
    def update_gem(self, new_state: GemState)-> None:
        'If it contains a gem it will update it, it will no nothing otherwise'

        if self.contains_gem():
            self._content.update_state(new_state)

    def contains_gem(self)-> bool:
        'Returns true if the cell contains a gem'

        return type(self._content) == Gem

    def is_valid_content(self, content: Gem|str)->bool:
        'Returns whether the content is valid for a cell'

        match content:
            case Gem():
                return content.is_valid_color(content.get_color())
            case str():
                return content == EMPTY

        return False
            

