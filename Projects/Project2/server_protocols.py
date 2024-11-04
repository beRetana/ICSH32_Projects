# This module contains functions that can be used to
# communicate with the I32CFSP server using it's protocol.

import server_connection

_CONNECTION = server_connection.ServerConnection()
_NOT_EXPECTED = "DID NOT RECEIVE THE EXPECTED INPUT FROM SERVER"
_CLOSED = "CONVERSATION CLOSED"


def new_conversation(user_name: str, server_address: tuple[str, int])-> str:
    '''Tries to start a conversation with the server,
       returns string with the coversation status'''

    if (" " in user_name) or ("\t" in user_name):
        return "NOT A VALID USERNAME"

    if _check_fail_state(_CONNECTION.connect_to_server(server_address)):
        return "FAILED TO CONNECT WITH SERVER"

    if _check_fail_state(_CONNECTION.write_to_server("I32CFSP_HELLO " + user_name)):
        end_conversation()
        return "FAILED TO WRITE TO SERVER"

    if _read_server_input() != ('WELCOME ' + user_name):
        end_conversation()
        return _NOT_EXPECTED

    return "TALKING"


def end_conversation()-> None:
    "Ends current conversation with the server if it's open"

    if _CONNECTION.is_connection_open():
        _CONNECTION.close_connection()

    
def start_game(columns: int, rows: int)-> str:
    'Start a new game with the server'

    if not _CONNECTION.is_connection_open():
        return _CLOSED

    if (4 <= columns <= 20 and  4 <= rows <= 20):
        _CONNECTION.write_to_server(f"AI_GAME {columns} {rows}")
        
        if _read_server_input() != "READY":
            return _NOT_EXPECTED
        
        return "GAME HAS STARTED"
    else:
        return "ENTERED AN INVALID SIZE"


def drop_piece(column: int, column_max_size: int)-> tuple[str, str]:
    '''Tell the server that a piece has been dropped in a specified column,
       returns the answer from the server or a failed state'''

    if _CONNECTION.is_connection_open():
        response = _make_move("DROP", column, column_max_size)
        return response

    return (_CLOSED, "")
    

def pop_piece(column: int, column_max_size: int)-> tuple[str, str]:
    '''Tell the server that a piece has been popped in a specified column,
       returns the answer from the server or a failed state'''

    if _CONNECTION.is_connection_open():
        response = _make_move("POP", column, column_max_size)
        return response

    return (_CLOSED, "")


# private functions that should not be used outside of this module

def _make_move(move_type: str, column: int, column_max_size: int)-> tuple[str, str]:
    '''Sends a move to the server and returns the appropiate
       response from the server based on the case.
       Returns the server's response or failed status'''

    user_input = f"{move_type} {column}"
    
    if(1 <= column <= column_max_size):
        
        if _check_fail_state(_CONNECTION.write_to_server(user_input)):
            return ("FAILED TO WRITE TO SERVER", user_input)

        server_input = _read_server_input()

        match(server_input):
            
            case "INVALID":
                _read_server_input()
                return ("INVALID INPUT", user_input)
            
            case "WINNER_RED" | "WINNER_YELLOW":
                
                if server_input == "WINNER_RED":
                    end_conversation()
                    return ("WINNER IS RED", "")
                elif server_input == "WINNER_YELLOW":
                    end_conversation()
                    return ("WINNER IS YELLOW", "")
            
            case "OKAY":
                server_move = _read_server_input()

                server_status = _read_server_input()

                if server_status == "WINNER_RED":
                    end_conversation()
                    return ("WINNER IS RED", server_move)
                elif server_status == "WINNER_YELLOW":
                    end_conversation()
                    return ("WINNER IS YELLOW", server_move)
                elif server_status != "READY":
                    end_conversation()
                    return (_NOT_EXPECTED, server_status)

                return (server_status, server_move)
            case _:
                end_conversation()
                return (_NOT_EXPECTED, server_input)
        
    else:
        return ("INVALID INPUT", user_input)
    

def _check_fail_state(state: str)-> bool:
    '''checks if the command failed'''

    failed = "FAILED"
    
    return failed in state


def _read_server_input()-> str:
    '''Gets input from server'''

    server_input = _CONNECTION.read_from_server()

    return server_input
    

    
