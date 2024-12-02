# project4.py

# Contains shell game management

import sys
import columns_game
import costume_exceptions
from cell import Location, Cell
from gem import GemState

_QUIT = "Q"

def _take_user_input()-> str:
    'Takes input from user and returns it as a string'
    
    user_input = input()
    
    if _QUIT == user_input:
        sys.exit()

    return user_input

def _take_field_size()-> tuple[int,int]:
    'Asks the user to input two ints and returns them'

    row = _take_user_input()
        
    column = _take_user_input()

    return (int(row), int(column))

def create_columns_game(size: tuple[int,int])-> columns_game.ColumnsGame:
    'Creates a new game using parameters and return it'

    row, column = size

    if row < 3 or column < 1:
        raise costume_exceptions.WrongFieldSize("SIZE FOR THE FIELD SHOULD BE 3X1 MINIMUM")
        sys.exit()

    try:
        new_game = columns_game.ColumnsGame(size)

    except costume_exceptions.WrongFieldSize:
        raise costume_exceptions.WrongFieldSize()
        sys.exit()
    else:
        return new_game

def _take_contents_input(rows_num: int)-> list[list[str]]:
    'Takes a sequence of lines as input and returns them as a list of list of strings'

    contents = []
    
    for num in range(rows_num):
        input_line = _take_user_input()
        content_row = []
        for char in input_line:
            content_row.append(char)
        contents.append(content_row)

    return contents

def _print_game_state(game: columns_game.ColumnsGame)->None:
    'prints the game state'
    
    formated_game_field = game.get_formated_game_state()
    for line in formated_game_field:
        print(line)

def _start_game(size, game_mode, content_list)-> columns_game.ColumnsGame:
    'Simulates taking input from the console'

    faller_index = 2
    column = 0
    matches = []

    rows, columns = size

    game = create_columns_game((rows, columns))

    if game_mode == "EMPTY":
        game.create_empty()
    elif game_mode == "CONTENTS":
        contents = content_list
        game.create_contents(contents)
        matches = game.check_field_matches()
        if len(matches) > 2:
            game._update_matching_gems(matches)
    else:
        raise costume_exceptions.WrongGameMode()

    _print_game_state(game)

    return (game, matches, column, faller_index)
    
def _test_game_loop(game: columns_game.ColumnsGame, matches: list[Cell], column: int, faller_index: int, commands: list[str])->None:
    'Testing Gameloop with preditermined inputs'

    for command in commands:

        if command == "":

            game.fallen_to_frozen()
            game.turn_to_fallen()
            game.drop_faller_once()

            if len(matches) > 0:
                game._eliminate_cells(matches)
                game.drop_frozen_gems()
                game.drop_faller_once()
                matches = []
                _print_game_state(game)
                continue
            else:
                matches = game.check_field_matches()
                if len(matches) > 0:
                    game._update_matching_gems(matches)
                    _print_game_state(game)
                    continue

            if game.get_faller_index() >= 0: 
                valid = game.drop_in_faller(Location(0,game.get_faller_column()), game.get_faller_index())

                game.set_faller_index(game.get_faller_index()-1)
                    
                if not valid:
                    game.turn_to_fallen()
                    game.fallen_to_frozen()
                    _print_game_state(game)
                    print("GAME OVER")
                    return

            _print_game_state(game)
            continue  
        
        match command[0]:
            case "F":
                if not game.is_there_faller(): 
                    key, column, top, middle, bottom = command.split(sep=" ")
                    game._create_faller(top, middle, bottom)
                    game.set_faller_column(int(column)-1)
                    game.set_faller_index(2)
                    
                    valid = game.drop_in_faller(Location(0,game.get_faller_column()), game.get_faller_index())
                    
                    if not valid:
                        game.turn_to_fallen()
                        game.fallen_to_frozen()
                        print("GAME OVER")
                        return
                
                    game.set_faller_index(1)
                    game.turn_to_fallen()
                    _print_game_state(game)
                    continue

            case "<":
                faller = game.get_faller()
                if faller != None:
                    if game.move_left():
                        game.set_faller_column(game.get_faller_column()-1)
                        game.turn_to_fallen()
                        _print_game_state(game)
            case ">":
                faller = game.get_faller()
                if faller != None:
                    if game.move_right():
                        game.set_faller_column(game.get_faller_column()+1)
                        game.turn_to_fallen()
                        _print_game_state(game)
            case "R":
                if len(game.get_faller()) < 3:
                    continue
                faller = game.get_faller()
                if faller != None:
                    game.rotate_faller()
                    game.turn_to_fallen()
                    _print_game_state(game)

def testing_cases(size, game_mode, commands, contents)-> None:
    'Simulates player input'

    game, matches, column, faller_index = _start_game(size, game_mode, contents)

    _test_game_loop(game, matches, column, faller_index, commands)


def _game_loop()->None:
    'Handles the logic for the gameloop'

    matches = []

    rows, columns = _take_field_size()

    game = create_columns_game((rows, columns))

    game_mode = _take_user_input()

    if game_mode == "EMPTY":
        game.create_empty()
    elif game_mode == "CONTENTS":
        contents = _take_contents_input(rows)
        game.create_contents(contents)
        matches = game.check_field_matches()
        if len(matches) > 2:
            game._update_matching_gems(matches)
    else:
        raise costume_exceptions.WrongGameMode()

    _print_game_state(game)

    while True:

        command = _take_user_input()

        if command == "":

            game.fallen_to_frozen()
            game.drop_faller_once()
            game.turn_to_fallen()

            if len(matches) > 0:
                game._eliminate_cells(matches)
                game.drop_frozen_gems()
                game.drop_faller_once()
                matches = []
                matches = game.check_field_matches()
                if len(matches) > 0:
                    game._update_matching_gems(matches)
                    _print_game_state(game)
                continue
            else:
                matches = game.check_field_matches()
                if len(matches) > 0:
                    game._update_matching_gems(matches)
                    _print_game_state(game)
                    continue

            if game.get_faller_index() >= 0: 
                valid = game.drop_in_faller(Location(0,game.get_faller_column()), game.get_faller_index())

                game.set_faller_index(game.get_faller_index()-1)
                    
                if not valid:
                    game.turn_to_fallen()
                    game.fallen_to_frozen()
                    _print_game_state(game)
                    print("GAME OVER")
                    return

            _print_game_state(game)
            continue  
        
        match command[0]:
            case "F":
                if not game.is_there_faller(): 
                    key, column, top, middle, bottom = command.split(sep=" ")
                    game._create_faller(top, middle, bottom)
                    game.set_faller_column(int(column)-1)
                    game.set_faller_index(2)
                    
                    valid = game.drop_in_faller(Location(0,game.get_faller_column()), game.get_faller_index())
                    
                    if not valid:
                        game.turn_to_fallen()
                        game.fallen_to_frozen()
                        print("GAME OVER")
                        return
                
                    game.set_faller_index(1)
                    game.turn_to_fallen()
                    _print_game_state(game)
                    continue

            case "<":
                faller = game.get_faller()
                if faller != None:
                    if game.move_left():
                        game.set_faller_column(game.get_faller_column()-1)
                        game.turn_to_fallen()
                        _print_game_state(game)
            case ">":
                faller = game.get_faller()
                if faller != None:
                    if game.move_right():
                        game.set_faller_column(game.get_faller_column()+1)
                        game.turn_to_fallen()
                        _print_game_state(game)
            case "R":
                if len(game.get_faller()) < 3:
                    continue
                faller = game.get_faller()
                if faller != None:
                    game.rotate_faller()
                    game.turn_to_fallen()
                    _print_game_state(game)
    

## Create the rest of the gameloop, user input, and gamestate printing




if __name__ == '__main__':
    _game_loop()





    
