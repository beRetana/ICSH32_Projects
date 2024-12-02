# test_gems_cells_game_state.py

import unittest
from columns_game import *
from gem import GemState
from cell import Location

class TestGameState(unittest.TestCase):

    def test_consecutive_drops(self):
        game = ColumnsGame((4,4))
        contents = [[" ", " ", " ", " "],
                    [" ", " ", " ", " "],
                    [" ", " ", " ", " "],
                    [" ", " ", " ", " "]]

        game.create_empty()
        game._create_faller("V", "W", "S")
        self.assertEqual(game.drop_in_faller(Location(0,3), 2), True)

if __name__ == '__main__':
    unittest.main()
        
