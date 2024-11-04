
from collections import namedtuple

def start_shell_game()-> None:
    'This function runs the gameloop of the game'

    from common_interactions_ui import start_game, GameInfo, get_user_move, PlayerMove, make_move, print_board
    from connectfour import winner

    game_information = start_game()
    
    while True:

        if(game_information.game_state.turn == 1):
            player_name = "RED"
        else:
            player_name = "YELLOW"

        print(f"PLAYER {player_name} MAKE YOUR MOVE!")

        player_move = get_user_move(game_information, game_information.game_state.turn)

        print("")

        game_information = GameInfo(make_move(game_information.game_state, player_move), game_information.size)

        possible_winner = winner(game_information.game_state)

        if(possible_winner != 0):
            print_winner = ""
            if possible_winner == 1:
                print_winner += "RED"
            elif possible_winner == 2:
                print_winner += "YELLOW"

            print(f'PLAYER {print_winner} HAS WON THE GAME!')
            break
        

if __name__ == "__main__":
    start_shell_game()

