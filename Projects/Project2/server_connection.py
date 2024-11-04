# This module contains a class that handles the connection to a server.

import socket

class ServerConnection:
    '''This class handles interactions with a given server'''

    def __init__(self):
        'Creates necessary private atributes for the object'
        
        self._input_from_server = None
        self._output_to_server = None
        self._server_socket = socket.socket()
        self._server_address = None
        

    def connect_to_server(self, server_address: tuple[str, int])-> str:
        '''Tries to establish a connection with the given server,
           returns a string reporting the status of the connection'''
        
        try:
            self._server_socket.connect(server_address)
        except:
            self._server_socket.close()
            return "FAILED TO CONNECT"
        else:
            self._input_from_server = self._server_socket.makefile("r")
            self._output_to_server = self._server_socket.makefile("w")
            self._server_address = server_address
            return "CONNECTED"


    def close_connection(self)-> str:
        '''Tries to close the connection with the current server,
           returns a string reporting the status of the action'''

        try:
            self._input_from_server.close()
            self._output_to_server.close()
            self._server_socket.close()
        except:
            return "FAILED TO CLOSE CONNECTION"
        else:
            return "CLOSED CONNECTION"
        

    def write_to_server(self, message: str)-> str:
        '''Tries to send commands to the current server,
           returns a string reporting the status of the action'''
        
        try:
            self._output_to_server.write( message + '\r\n')
            self._output_to_server.flush()
        except:
            return "FAILED TO WRITE TO SERVER"
        else:
            return "SENT"

    def read_from_server(self)-> str:
        '''Tries to read input from the current server,
           returns a string reporting a FAILED case or the input'''

        try:
            message = self._input_from_server.readline()[:-1]
        except:
            return "FAILED TO READ FROM SERVER"
        else:
            return message

    def is_connection_open(self)-> bool:
        '''Checks if there are files assosiated with the socket,
           if not returns True meaning the socket is closed'''

        if self._server_socket.fileno() == -1:
            return False

        return True
          
