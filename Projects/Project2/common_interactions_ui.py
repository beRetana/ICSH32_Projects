# This module contains functions that both games can use.
from connectfour import GameState, drop, pop
from collections import namedtuple

GameInfo = namedtuple("GameInfo", ["game_state", "size"])
BoardSize = namedtuple("BoardSize", ["columns", "rows"])
PlayerMove = namedtuple("PlayerMove", ["command", "column"])

def _string_to_int(word: str)-> int:
    '''Tries to convert a string into an int, returns -1
       if not possible and the word as an int otherwise'''

    number = 0

    try:
        number = int(word)
    except:
        return -1
    else:
        return number


def _spacer(index: int, max_index: int, middle: int)-> str:
    '''Takes an int and returns a string with the
       appropiate number of spaces'''

    if index >= max_index:
        return ""
            
    elif index > middle:
        return ' '
            
    else:
        return '  '

            
def _index_header(columns: range)-> str:
    '''Makes a string with the indexes and corresponing spaces
     returns that string'''

    column_index_count = 0

    column_index_string = ""

    for column in columns:

        column_index_count += 1

        next_index = f'{column_index_count}{_spacer(column_index_count, len(columns), 8)}'

        column_index_string += next_index

    return column_index_string

def _row_maker(board: GameState.board)-> list[str]:
    '''Makes the rows of the board into strings and returns it'''

    rows = []

    row_index = 0

    first_column = board[0]

    for row in first_column:

        column_index = 1

        row_string = ""

        for column in board:

            spaces = _spacer(column_index, len(board), len(board))

            match column[row_index]:
                case 0:
                    row_string += f'.{spaces}'
                case 1:
                    row_string += f'R{spaces}'
                case 2:
                    row_string += f'Y{spaces}'

            column_index += 1

        rows.append(row_string)

        row_index += 1

    return rows


def _check_valid_drop(columns: list[int])-> bool:
    '''Checks if dropping a coin in that column is a valid move'''
    
    for index in range(len(columns)-1, -1,-1):
        if columns[index] == 0:
            return True

    return False

def _check_valid_pop(columns: list[int], player: int)-> bool:
    '''Checks if dropping a coin in that column is a valid move'''

    if columns[len(columns)-1] == player:
        return True

    return False
    

#----------------------Public functions are below-----------------------


def input_string(message: str)-> str:
    '''Takes input from the player with a message embeded,
       returns a cleaned version of the input'''

    player_input = ""

    while True:
        
        player_input = input(f'{message}: ').strip().upper()

        if player_input != "":
            break

    return player_input


def input_int(message: str, max_num: int, min_num: int)-> int:
    '''Asks the player for input as int and returns it as an it,
       if the player doesn't enter a positive integer, it will ask
       again until a number is typed'''

    player_input = 0

    while True:

        player_input = _string_to_int(input_string(message))

        if min_num <= player_input <= max_num:
            break

        print(f"ERROR: Please enter an integer within {min_num}-{max_num}")

    return player_input

def print_welcome()-> None:
    'Prints a nice title for players to understand what the game is about'
    
    print("WELCOME TO CONNECT 4 POP-OUT FOR ICS H32 FALL 2024")
    print("--------------------------------------------------")
    print("A game where you create a costume sized board:")
    print("MAX SIZE     COL: 20, ROW: 20")
    print("MIN SIZE     COL:  4, ROW:  4\n")
    print("You always act first, you can:")
    print("  * DROP a disc in a column: 'D 3'")
    print("  * POP a bottom disc from a column: 'P 2'\n")


def get_board_size()-> BoardSize:
    '''Gets the board size from the '''

    column_size = input_int("ENTER COLUMN SIZE", 20, 4)

    row_size = input_int("ENTER ROW SIZE", 20, 4)

    return BoardSize(column_size, row_size)


def print_board(game_state: GameState)-> None:
    'Prints the current game state'

    column_index_string = _index_header(range(len(game_state.board)))

    print(column_index_string)

    rows = _row_maker(game_state.board)

    for line in rows:
        print(line)

    print("")


def get_user_move(game_info: GameInfo, player: int)-> PlayerMove:
    '''Gets input from the player in the format specified'''

    column_num = game_info.size.columns

    while True:

        user_input = input_string("ENTER YOUR MOVE [D]ROP or [P]OP")

        if(3 <= len(user_input) <= 4 and user_input[1] == " "):
            command = user_input[0]
            column_selected = _string_to_int(user_input[2:])
            
            if 1 <= column_selected <= column_num:
                
                match (command):
                    
                    case 'P':
                        if _check_valid_pop(game_info.game_state.board[column_selected-1], player):
                            return PlayerMove(command, column_selected)
                        
                        else:
                            print("ERROR: NOT A VALID POP (YOUR DISC IS NOT AT THE BOTTOM)")
                            continue
                        
                    case 'D':
                        if _check_valid_drop(game_info.game_state.board[column_selected-1]):
                            return PlayerMove(command, column_selected)
                        
                        else:
                            print("ERROR: NOT A VALID DROP (COLUMN IS FULL)")
                            continue
                        
                    case _:
                        print(f'ERROR: ENTER A COMMAND "D" or "P"')
                        continue
                
            else:
                print(f'ERROR: ENTER A VALUE FROM 1 TO {column_num}')
                continue
                    
        print('ERROR: ENTER MOVE IN FORMAT "D 3"')


def make_move(game_state: GameState, player_move: PlayerMove)-> GameState:
    '''Updates the game with the move provided prints it and
       returns the updated game state'''

    new_game_state = None

    match player_move.command:
        case "D":
            new_game_state = drop(game_state, player_move.column-1)
        case "P":
            new_game_state = pop(game_state, player_move.column-1)

    print_board(new_game_state)

    return new_game_state
        

def start_game()-> GameInfo:
    'Hadles the printing an logic for starting a game'

    from connectfour import new_game

    print_welcome()

    board_size = get_board_size()    

    game_state = new_game(board_size.columns, board_size.rows)

    print("")

    print_board(game_state)

    print("THIS WILL BE YOUR NEW CONNECT FOUR BOARD\n")

    return GameInfo(game_state, board_size)



    

