# columns_game.py

# Handles the logic for creating a Columns Game
# object that takes care of managing the game state.

from costume_exceptions import WrongFieldSize, WrongContentInput, WrongCellValue
from enum import Enum
from gem import Gem, GemState
from cell import Cell, EMPTY, Location
   
# Macro-manages the game state using functions to create changes in the object
# this is to avoid cupling with the user interface module.

class ColumnsGame:

    def __init__(self, size: tuple[int,int]):
        rows, columns = size
        
        if rows < 3 or columns < 1:
            raise WrongFieldSize()
        
        self._rows = rows
        self._columns = columns
        self._game_state = []
        self._faller = []
        self._faller_index = 0
        self._faller_column = 0
        self._triple = False

    def get_game_size(self)-> tuple[int,int]:
        'Returns the size of the field as a tuple'
        
        return (self._rows, self._columns)
    
    def get_faller_column(self)-> int:
        return self._faller_column
    
    def get_faller_index(self)-> int:
        return self._faller_index
    
    def set_faller_column(self, value: int)-> None:
        self._faller_column = value

    def set_faller_index(self, value: int)-> None:
        self._faller_index = value

    def get_game_state(self)-> list[list[Cell]]:
        'Returns the game state'

        return self._game_state

    def get_formated_game_state(self)->list[str]:
        'Returns the game state in a string formated list'

        if len(self._game_state) < 1:
            return "EMPTY"

        formated_game_state = []

        for row in self._game_state:
            formated_row = "|"
            for cell in row:
                formated_row += cell.get_formated_content()
            formated_row += "|"
            formated_game_state.append(formated_row)

        last_line = " " + "-"*self._columns*3 + " "
        formated_game_state.append(last_line)

        return formated_game_state
        
    def create_empty(self)-> None:
        'Creates a new empty field and stores it as the game state'

        field = []

        for row in range(self._rows):
            new_row = []
            for column in range(self._columns):
                new_row.append(Cell(Location(row, column)))
            field.append(new_row)

        self._game_state = field

    def create_contents(self, new_game_state: list[list[str]])-> None:
        'Inserts gems into the field and update the game state'

        if len(new_game_state) != self._rows:
            raise WrongContentInput("Wrong Row Size")
        else:
            for row in new_game_state:
                if len(row) != self._columns:
                    raise WrongContentInput("Wrong Column Size")

        self.create_empty()

        for row_index in range(len(new_game_state)):
            for column_index in range(len(new_game_state[row_index])):
                content_input = new_game_state[row_index][column_index]
                cell = self._get_cell_at(Location(row_index, column_index))
                if self._is_valid_input(content_input):
                    if content_input != " ":
                        gem = Gem(content_input)
                        gem.update_state(GemState.FROZEN)
                        cell.add_content(gem)

                else:
                    WrongCellValue("Wrong Value For A Cell When Creating Contents")

        self.drop_frozen_gems()

    def fallen_to_frozen(self)->None:
        'Turns all fallen gems to a frozen state'

        for row in self._game_state:
            for cell in row:
                if cell.contains_gem() and cell.peek_content().get_state() == GemState.FALLER_LANDED:
                    cell.peek_content().update_state(GemState.FROZEN)


    def drop_faller_once(self)->None:
        'Makes Fallers drop down by one cell'

        for row in range(len(self._game_state)-2,-1,-1):
            for cell in self._game_state[row]:
                if cell.contains_gem():
                    if cell.peek_content().get_state() == GemState.FALLER:
                        row, column = cell.get_location()
                        new_cell = self._game_state[row+1][column]
                        new_cell.pop_content(cell.pop_content())

    def turn_to_fallen(self)->None:
        'Looks for gems that are FALLERs and turns them into FALLEN'
        for row in reversed(range(len(self._game_state))):
            for col in range(len(self._game_state[row])):
                cell = self._game_state[row][col]
                if cell.contains_gem() and cell.peek_content().get_state() == GemState.FALLER:
                    if row < self._rows-1 and col < self._columns:
                        bottom_cell = self._game_state[row+1][col]
                        if bottom_cell.contains_gem():
                         if bottom_cell.peek_content().get_state() == GemState.FROZEN or bottom_cell.peek_content().get_state() == GemState.FALLER_LANDED:
                            cell.peek_content().update_state(GemState.FALLER_LANDED)
                    elif row == self._rows-1:
                        cell.peek_content().update_state(GemState.FALLER_LANDED)        
        

    def is_there_fallen(self)->bool:
        'Returns true if the game contains a fallen gems'

        for row in self._game_state:
            for cell in row:
                if cell.contains_gem() and cell.peek_content().get_state() == GemState.FALLER_LANDED:
                    return True
        return False

    def drop_frozen_gems(self)-> None:
        "Makes all frozen gems fall if they don't have another gem under"

        for row in range(len(self._game_state)-1, -1,-1):
            for column in range(len(self._game_state[row])):
                cell = self._get_cell_at(Location(row, column))
                if cell.contains_gem():
                    if cell.peek_content().get_state() == GemState.FROZEN:
                        self._drop_gem_to_bottom(Location(row, column))

    def rotate_faller(self)-> None:
        'Rotates the gems in the faller'

        top, middle, bottom = self._faller

        top_color = top.get_color()
        middle_color = middle.get_color()
        bottom_color = bottom.get_color()

        top.set_color(bottom_color)
        middle.set_color(top_color)
        bottom.set_color(middle_color)

        self._faller = [top, middle, bottom]

    def get_faller(self)->None:
        'Returns the value of the faller'

        return self._faller

    def is_there_faller(self)-> bool:
        'Returns if there is a faller gem'

        for row in self._game_state:
            for cell in row:
                if cell.contains_gem(): 
                    if cell.peek_content().get_state() == GemState.FALLER or cell.peek_content().get_state() == GemState.FALLER_LANDED:
                        return True
        return False
    

    def move_right(self)->bool:
        'Moves fallers to the right if possible'
        return self._move_cells(1)

    def move_left(self)->bool:
        'Moves fallers to the left if possible'
        return self._move_cells(-1)
        

    def _move_cells(self, column_delta)->bool:
        'Moves fallers if possible'

        faller_cells = []

        for row in self._game_state:
            for cell in row:
                if cell.contains_gem():
                    state = cell.peek_content().get_state()
                    if state == GemState.FALLER or state == GemState.FALLER_LANDED:
                        faller_cells.append(cell)

        for cell in faller_cells:
            row, new_col = cell.get_location()
            new_col += column_delta
            if self._game_state[row][new_col].contains_gem():
                return False

        for cell in faller_cells:
            row, new_col = cell.get_location()
            new_col += column_delta
            if -1 < new_col < self._columns:
                self._game_state[row][new_col].pop_content(cell.pop_content())
            else:
                return False
        
        return True
        
                

    def drop_in_faller(self, location: Location, index: int)->bool:
        'Tries to drop in faller gems, if it fails it will end the game'
    
        # Is there's a gem in the cell?
        cell = self._game_state[0][location.column]
        if cell.contains_gem():
            # Yes: Is ther a matching gem around?
            is_matching_gem = False
            for column in range(-1, 2):
                col_index = location.column + column
                if 0 <= col_index < len(self._game_state[0]):  # Ensure within column bounds
                    cell_to_check = self._game_state[0][col_index]
                    if cell_to_check.contains_gem():
                        if cell_to_check.peek_content().get_color() == self._faller[index].get_color():
                            is_matching_gem = True
            if is_matching_gem:
                # Yes: Is the an immidiate match?
                if self.check_immidiate_match(location, index):
                    return True
                else:
                    return False
                    # No: End Game
            else:
                return False
                # No: End Game
        else:
            self._game_state[location.row][location.column].pop_content(self._faller[index])
            return True
            # No: Insert gem then exit.
                        

    def check_immidiate_match(self, location: Location, index:int)-> bool:
        'Checks if there is an immidiate case for a match when faller spawned'

        bottom_cell = self._game_state[0][location.column]
        
        if self._faller[0].get_color() == self._faller[1].get_color() == self._faller[2].get_color():

            cell = Cell(Location(-1, location.column))
            cell.add_content(self._faller[index])
                
            other_matches = self.check_all_sides(cell)
                
            if bottom_cell.peek_content().get_color() == self._faller[index].get_color():
                if not bottom_cell in other_matches:
                    other_matches.append(bottom_cell)
                for index in range(len(self.get_faller())):
                    if self.get_faller()[index].get_state() == GemState.MATCH and self._triple:
                        self.drop_in_faller(Location(0,self.get_faller_column()), self.get_faller_index())
                        self.get_faller()[0].update_state(GemState.MATCH)
                        self.get_faller()[1].update_state(GemState.MATCH)
                        self.get_faller()[2].update_state(GemState.MATCH)
                        break
                self._update_matching_gems(other_matches)
                self._triple = True
                return True
            elif len(other_matches) > 1:
                self._update_matching_gems(other_matches)
                self._triple = True
                return True
            else:
                return False           
            
        elif index > 0 and self._faller[index-1].get_color() == self._faller[index].get_color():
                
            cell = Cell(Location(-1, location.column))
            cell.add_content(self._faller[index])
                
            other_matches = self.check_all_sides(cell)
                
            if bottom_cell.peek_content().get_color() == self._faller[index].get_color():
                if not bottom_cell in other_matches:
                    other_matches.append(bottom_cell)
                self._update_matching_gems(other_matches)
                self._faller = []
                return True
            elif len(other_matches) > 1:
                if index == 1:
                    self._update_matching_gems(other_matches)
                    self._faller = [self._faller[0]]
                    return True
                else:
                    self._update_matching_gems(other_matches)
                    self._faller = []
                    return True
            else:
                return False
            
        else:
            cell = Cell(Location(-1, location.column))
            cell.add_content(self._faller[index])
                
            other_matches = self.check_all_sides(cell)

            if len(other_matches) > 1:
                self._update_matching_gems(other_matches)
                self._faller = []
                return True
            else:
                return False


    def _update_matching_gems(self, cells_to_update: list[Cell])-> None:
        'Updates the states of the gems in the list to MATCH'

        for cell in cells_to_update:
            cell.peek_content().update_state(GemState.MATCH)
            row, column = cell.get_location()
            self._game_state[row][column] = cell


    def _eliminate_cells(self, cells_to_eliminate: list[Cell])-> None:
        'Pops all the gems inside the cells in the given list'

        for cell in cells_to_eliminate:
            cell.pop_content()


    def _check_matches(self, initial_cell: Cell, row_delta: int, column_delta: int)-> list[Cell]:
        'Returns a list of all the cells with a matching gem if any based on the direction given'
        
        matching_cells = []
        initial_location = initial_cell.get_location()
        
        if not (-1 < initial_location.row + row_delta < self._rows):
            return matching_cells

        if not (-1 < initial_location.column + column_delta < self._columns):
            return matching_cells

        initial_gem = initial_cell.peek_content()
        diagonal_cell = self._game_state[initial_location.row + row_delta][initial_location.column + column_delta]
        
        if diagonal_cell.contains_gem():
            diagonal_gem = diagonal_cell.peek_content()
            if initial_gem.get_color() == diagonal_gem.get_color():
                matching_cells.append(diagonal_cell)
                matching_cells += self._check_matches(diagonal_cell, row_delta, column_delta)

        return matching_cells

    def check_all_sides(self, initial_cell: Cell)-> list[Cell]:
        'Returns a list of all the cells with a matching gem if any'

        matches = []
        
        for row_delta in range(-1,2):
            for column_delta in range(-1,2):
                if row_delta == 0 and column_delta == 0:
                    continue
                
                possible_matches = self._check_matches(initial_cell, row_delta, column_delta)

                if len(possible_matches) > 1:
                    matches += possible_matches
                    
        return matches


    def check_field_matches(self)-> list[Cell]:
        'Checks all matches for all cells in the field'

        possible_matches = []
        
        for row in self._game_state:
            for cell in row:
                if cell.contains_gem() and cell.peek_content().get_state() == GemState.FROZEN:
                    possible_matches += self.check_all_sides(cell)

        return possible_matches
        
        
    def _create_faller(self, top: str, middle: str, bottom: str)-> None:
        'Returns a tuple with three gems in the respective order of the colors given'

        gem_faller = [Gem(top), Gem(middle), Gem(bottom)]

        for gem in gem_faller:
            gem.update_state(GemState.FALLER)

        self._faller = gem_faller
    

    def _drop_gem_to_bottom(self, location: Location)->None:
        'Gets the gem inside and drops it to the lowest point possible'

        if location.row == self._rows-1:
            return

        cell = self._get_cell_at(location)
        cell_below = self._get_cell_at(Location(location.row+1, location.column))
        
        if cell_below.peek_content() == EMPTY:
            cell_below.pop_content(cell.pop_content())
            self._drop_gem_to_bottom(Location(location.row+1, location.column))
        else:
            return       

    def _get_cell_at(self,location: Location)-> Cell:
        'Receives the location of a cell in the field and returns the cell'

        return self._game_state[location.row][location.column]

    def _is_valid_input(self, content_input: str)-> bool:
        'Returns whether the string is a valid input for a cell/gem'

        match content_input:
            case " ":
                return True
            case _:
                return Gem.is_valid_color(Gem,content_input)

    # Needs to implement FALLERS, generating gems with their colors and
    # updating the game state frame by frame. Also loading a game state









        
        
        
