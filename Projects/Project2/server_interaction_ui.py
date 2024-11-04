

import server_protocols
import common_interactions_ui
import connectfour
from collections import namedtuple
from common_interactions_ui import GameInfo, PlayerMove, BoardSize

    
def get_username()-> str:
    'Gets a valid username from the player'

    from common_interactions_ui import input_string

    while True:

        username = input_string("ENTER A USERNAME")

        if not username.isascii():
            print("ERROR: USERNAME SHOULD ONLY HAVE ASCII CHARACTERS")
            continue

        if username.find(" ") == -1:
            break
        else:
            print("ERROR: USERNAME SHOULD NOT HAVE SPACES")
    
    return username


def get_host()-> str:
    'Gets the host for the server from the user'

    from common_interactions_ui import input_string

    real_host = "circinus-32.ics.uci.edu"

    while True:

        host = input_string("ENTER THE HOST FOR THE SERVER").lower()

        if host == real_host:
            break

        print("YOUR INPUT DOES NOT MATCH THE VALID HOST")
    
    return host


def get_port()-> int:
    'Gets the port for the server from the user'

    from common_interactions_ui import input_int

    real_port = 4444

    while True:

        port = input_int("ENTER THE PORT FOR THE SERVER", 65535, 1)

        if port == real_port:
            break

        print("YOUR INPUT DOES NOT MATCH THE VALID PORT")
    
    return port


def set_connection()-> tuple[bool, str]:
    '''Gets sever IP and port number from user and
       returns whether the program connected successfully to the server'''

    from server_protocols import new_conversation

    host = get_host()
    port = get_port()
    username = get_username()

    conversation_status = new_conversation(username, (host, port))

    if conversation_status != "TALKING":
       print(f"ERROR: {conversation_status}")
       return (False, username)

    return (True, username)


def player_move_to_server(player_move: PlayerMove, game_size: BoardSize)-> tuple[str, str]:
    '''Takes the player's move and sends that information to the server
       returns the state of trying that action'''

    match player_move.command:
        case "D":
            response = server_protocols.drop_piece(player_move.column, game_size.columns)
        case "P":
            response = server_protocols.pop_piece(player_move.column, game_size.columns)
        case _:
            response = ("PLAYER MOVE NOT RECOGNIZED", f'{player_move.command} {player_move.column}')
    
    return response


def check_server_action(action_check: tuple[str, str])->bool:
    '''Checks if the server response have any of the key words that
       are used to define a failed state'''

    if action_check[0].find("INVALID") != -1:
        if action_check[0].find("FAILED") != -1:
            if action_check[0].find("EXPECTED") != -1:
                return False

    return True


def game_set_up() -> tuple[GameInfo, str] | None:
    'Function takes care of setting up the beginning of the game'

    is_connected, username = set_connection()

    print("")

    if not is_connected:
        return
    else:
        print("CONNECTED SUCCESFULLY!\n")

    game_information = common_interactions_ui.start_game()

    ai_game_started = server_protocols.start_game(game_information.size.columns, game_information.size.rows)

    if ai_game_started != "GAME HAS STARTED":
        print(f"ERROR: {ai_game_started}")
        return

    print("NOW THAT YOUR BOARD IS SET UP YOU WILL PLAY AGAINST AN AI!\n")

    return game_information, username


def player_turn(game_information: GameInfo, username: str) -> tuple[GameInfo, PlayerMove, int]:
    '''Takes player move and updates the game, returns the updated game,
       player's move and if there was a winner'''

    print(f"PLAYER RED: {username} MAKE YOUR MOVE!")
    
    print("")

    ## TAKE HUMAN INPUT AS TUPLE[COMMAND, COLUMN]
    player_move = common_interactions_ui.get_user_move(game_information, game_information.game_state.turn)

    print("")

    ## UPDATE THE GAME WITH USER'S MOVE AND GET UPDATED GAME INFO
    game_information = GameInfo(common_interactions_ui.make_move(game_information.game_state, player_move), game_information.size)

    ## CHECK FOR WINNER
    is_winner = connectfour.winner(game_information.game_state)

    return (game_information, player_move, is_winner)

    
def ai_turn(game_information: GameInfo, server_action) -> tuple[GameInfo | None, bool]:
    '''Takes game information and the server's action to
       generate the ai's move, return the new game information
       and the server's move or None in case of failure'''

    if server_action[1] != "":

        print(f"PLAYER YELLOW: AI IS MAKING IT'S MOVE!")

        print("")

        print(f"AI'S MOVE IS: {server_action[1]}")
        
        print("")

        server_move = server_action[1].split()

        server_move = PlayerMove(server_move[0][0], common_interactions_ui._string_to_int(server_move[1]))
        
        game_information = GameInfo(common_interactions_ui.make_move(game_information.game_state, server_move), game_information.size)

    ## CHECK FOR WINNER
    is_winner = connectfour.winner(game_information.game_state)

    return (game_information, is_winner)


def is_there_winner(server_action: tuple[str,str], is_winner: int, username: str) -> bool:

    ### IF SERVER SAYS THERE'S A WINNER
    if server_action[0].find("WINNER") != -1:
        ### IF SERVER AND GAME STATE SAY RED WON
        if server_action[0].find("RED") != -1 and is_winner == 1:
            print(f'PLAYER RED: {username} HAS WON THE GAME!')
            return True
        ### IF SERVER AND GAME STATE SAY YELLOW WON
        elif server_action[0].find("YELLOW") != -1 and is_winner == 2:
            print(f'PLAYER YELLOW: AI HAS WON THE GAME!')
            return True
        ### IF SERVER AND GAME STATE DON'T AGREE END GAME
        else:
            server_protocols.end_conversation()
            print(f'ERROR: DID NOT RECEIVE THE EXPECTED WINNER FROM SERVER')
            return None
    ### IF SERVER AND GAME STATE DON'T AGREE END GAME
    elif server_action[0].find("WINNER") == -1 and is_winner != 0:
        server_protocols.end_conversation()
        print(f'ERROR: DID NOT RECEIVE THE EXPECTED INPUT FROM SERVER')
        return None

    return False


def game_loop(game_information: GameInfo, username: str) -> None:
    '''Runs the gameloop of the game, each player inputs they moves and ends when there is a winner'''

    # Gameloop

    while True:

        # GAME IS NOW SET UP, PLAYERS MAKE THEIR MOVES

        ## Player's turn
        game_information, player_move, is_winner = player_turn(game_information, username)
        
        ## UPDATE SERVER WITH USER'S MOVE AND GET THE SERVER'S RESPONSE
        server_action = player_move_to_server(player_move, game_information.size)

        ## AI'S TURN TO MOVE
        game_information, is_winner = ai_turn(game_information, server_action)

        if(game_information == None):
            return
           
        ## CHECK IF SERVER SENT A WINNER

        is_winner = is_there_winner(server_action, is_winner, username)
        
        if is_winner or is_winner == None:
            return 
        
    
def start_online_game()-> None:
    'This function runs the gameloop of the game'

    ## SETTING UP THE GAME
    game_information, username = game_set_up()

    if(game_information == None):
        return

    game_loop(game_information, username)

if __name__ == "__main__":
    start_online_game()
