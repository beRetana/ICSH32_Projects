# test_project4.py

# Tests the functionality of helper functions
# for the shell game management.

import unittest
from project4 import *
from costume_exceptions import WrongFieldSize
import columns_game

class TestProject4 (unittest.TestCase):

    def test_handling_failing_to_create_a_new_game__wrong_parameters(self):
        with self.assertRaises(WrongFieldSize):
            create_columns_game((1,1))

    def test_creating_columns_game_of_squared_size(self):
        self.assertEqual(create_columns_game((4,4)).get_game_size(), (4,4))

    def test_series_of_random_commands_for_an_empty_field(self):
        'This is a series of prints of what a simulated interaction with the program would look like'
        size = (5,6)
        game_mode = "EMPTY"
        list_of_commands = ["F 3 Y T S",">","","<","","R","", "F 4 X V X", "<","<","<","","","","","F 4 X V X","","",">","<","Q"]
        testing_cases(size, game_mode, list_of_commands, [])

    def test_series_of_random_commands_for_a_populated_field(self):
        'This is a series of prints of what a simulated interaction with the program would look like'
        size = (4,4)
        game_mode = "CONTENTS"
        list_of_commands = ["F 3 X X X",">","","<","","R","", "F 4 X V X", "<","<","<","","","","","F 4 X V X","","",">","<","Q"]
        contents = [[" ","S","T"," "],
                    ["V"," "," ","W"],
                    ["X","X"," ","X"],
                    [" ","Z","Y"," "]]
        testing_cases(size, game_mode, list_of_commands, contents)


if __name__ == '__main__':
    unittest.main()
