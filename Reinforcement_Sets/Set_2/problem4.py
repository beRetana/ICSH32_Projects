import socket
import random

HOST = "circinus-32.ics.uci.edu"

PORT = 1564

def _connect_server(host: str, port: int) -> 'connection':
    'Creates a socket and connects to server'

    address = (host, port)
    connection_socket = socket.socket()
    connection_socket.connect(address)

    input_port = connection_socket.makefile('r')
    output_port = connection_socket.makefile('w')

    return input_port, output_port, connection_socket

def _disconnect_server(input_port: 'input port',
                       output_port:'output port',
                       connection_socket:'connection socket') -> None:
    'Closes down port connections and sockets'

    input_port.close()
    output_port.close()
    connection_socket.close()

def _random_number(upper: int | float)-> int:
    'Generates a random int between 0 and upper'
    
    return random.randint(0, int(upper))

def _server_interaction(input_port: 'input port',
                        output_port:'output port',
                        connection_socket:'connection socket')-> None:
    "Interacts with the server and prints out the server's responses"
    
    output_port.write('SHAKESPEARE_COUNTS\r\n')
    output_port.flush()
    numbers = input_port.readline()
        
    first_num = numbers[:numbers.find(" ")]
    numbers = numbers[numbers.find(" ")+1:]
        
    second_num = numbers[:numbers.find(" ")]
    numbers = numbers[numbers.find(" ")+1:]
        
    third_num = numbers[:-1]

    numbers = (_random_number(first_num),
                _random_number(second_num),
                _random_number(third_num))

    output_port.write(f'SHAKESPEARE_INSULT {numbers[0]} {numbers[1]} {numbers[2]}\r\n')
    output_port.flush()

    server_input = input_port.readline()[:-1]

    print(server_input)

    output_port.write("SHAKESPEARE_GOODBYE\r\n")
    output_port.flush()

    server_input = input_port.readline()[:-1]

    print(server_input)
        

def _run_program()-> None:
    'Calls functions to establish a connection, interact, and close connection'

    try:
        connection_components = _connect_server(HOST, PORT)

        if connection_components[2] != None:
            _server_interaction(connection_components[0], 
                                connection_components[1],
                                connection_components[2])
            
    except:
        print("There was an issue connecting to the server")

    finally:
        if connection_components[2] != None:
            _disconnect_server(connection_components[0], 
                                connection_components[1],
                                connection_components[2])
    

if __name__ == "__main__":
    _run_program()
    
