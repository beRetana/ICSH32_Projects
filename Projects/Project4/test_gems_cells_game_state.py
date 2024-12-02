# test_game_state.py

import unittest
from columns_game import *
from gem import GemState
from cell import Location

class TestGems(unittest.TestCase):

    def test_get_empty_formated_game_state(self):
        game = ColumnsGame((4,4))
        game.create_empty()
        expected = ["|            |",
                    "|            |",
                    "|            |",
                    "|            |",
                    " ------------ "]

        self.assertEqual(game.get_formated_game_state(), expected)
        

    def test_creating_contents_formated_game_state(self):
        game = ColumnsGame((4,4))
        contents = [[" ","S","T"," "],
                    ["V"," "," ","W"],
                    ["X","X"," ","X"],
                    [" ","Z","Y"," "]]
        
        expected_result = ["|            |",
                           "|    S       |",
                           "| V  X  T  W |",
                           "| X  Z  Y  X |",
                           " ------------ "]

        game.create_contents(contents)

        self.assertEqual(game.get_formated_game_state(), expected_result)


    def test_creating_contents_formated_game_state_combination_empty_non_squared(self):

        game = ColumnsGame((40,28))

        contents = []
        expected_result = []

        array = []
        expected = "|"

        for count in range(28):
            array.append(" ")
            expected += "   "

        expected += "|"

        for count in range(40):
            contents.append(array)
            expected_result.append(expected)
        
        game.create_contents(contents)

        last_line = " " + "-"*28*3 + " "
        expected_result.append(last_line)
        
        self.assertEqual(game.get_formated_game_state(), expected_result)


    def test_creating_contents_formated_game_state_combination_full_non_squared(self):

        game = ColumnsGame((40,15))

        contents = []
        expected_result = []

        array = []
        expected = "|"

        for count in range(15):
            array.append("S")
            expected += " S "

        expected += "|"

        for count in range(40):
            contents.append(array)
            expected_result.append(expected)
        
        game.create_contents(contents)
        last_line = " " + "-"*15*3 + " "
        expected_result.append(last_line)

        self.assertEqual(game.get_formated_game_state(), expected_result)
        

    def test_creating_contents_formated_game_state_combination_empty(self):

        game = ColumnsGame((4,4))
        contents = [[" ", " ", " ", " "],
                    [" ", " ", " ", " "],
                    [" ", " ", " ", " "],
                    [" ", " ", " ", " "]]
        
        expected_result = ["|            |",
                           "|            |",
                           "|            |",
                           "|            |",
                           " ------------ "]
        
        game.create_contents(contents)

        self.assertEqual(game.get_formated_game_state(), expected_result)


    def test_creating_contents_formated_game_state_combination_full(self):

        game = ColumnsGame((4,4))
        contents = [["S", "T", "S", "W"],
                    ["V", "V", "T", "X"],
                    ["Y", "Z", "X", "Y"],
                    ["Y", "Z", "X", "Y"]]
        
        expected_result = ["| S  T  S  W |",
                           "| V  V  T  X |",
                           "| Y  Z  X  Y |",
                           "| Y  Z  X  Y |",
                           " ------------ "]
        
        game.create_contents(contents)

        self.assertEqual(game.get_formated_game_state(), expected_result)


    def test_is_valid_input_should_be_true(self):
        self.assertEqual(ColumnsGame._is_valid_input(ColumnsGame," "), True)
        self.assertEqual(ColumnsGame._is_valid_input(ColumnsGame,"S"), True)
        self.assertEqual(ColumnsGame._is_valid_input(ColumnsGame,"T"), True)
        self.assertEqual(ColumnsGame._is_valid_input(ColumnsGame,"W"), True)
        self.assertEqual(ColumnsGame._is_valid_input(ColumnsGame,"Y"), True)
        self.assertEqual(ColumnsGame._is_valid_input(ColumnsGame,"Z"), True)
        self.assertEqual(ColumnsGame._is_valid_input(ColumnsGame,"A"), False)

    def test_check_matches_should_work(self):

        game = ColumnsGame((4,4))
        contents = [["S", "T", "V", "W"],
                    ["V", "V", "T", "X"],
                    ["V", "Z", "X", "Y"],
                    ["Y", "Z", "X", "Y"]]

        game.create_contents(contents)

        initial = game._game_state[0][2]

        matches = game._check_matches(initial, 1, -1)

        initial = [game._game_state[1][1], game._game_state[2][0]]

        self.assertEqual(matches, initial)

    def test_check_matches_return_empty(self):
        game = ColumnsGame((4,4))
        contents = [["S", "T", "V", "W"],
                    ["V", "Z", "T", "X"],
                    ["V", "Z", "X", "Y"],
                    ["Y", "Z", "X", "Y"]]

        game.create_contents(contents)

        initial = game._game_state[0][2]

        matches = game._check_matches(initial, 1, -1)

        initial = []

        self.assertEqual(matches, initial)


    def test_check_matches_from_all_sides_empty(self):
        
        game = ColumnsGame((4,4))
        contents = [["S", "T", "V", "W"],
                    ["V", "Z", "T", "X"],
                    ["V", "Z", "X", "Y"],
                    ["Y", "Z", "X", "Y"]]

        game.create_contents(contents)

        initial = game._game_state[0][2]

        matches = game.check_all_sides(initial)

        initial = []

        self.assertEqual(matches, initial)

    def test_check_matches_from_all_sides_not_empty(self):
        
        game = ColumnsGame((4,4))
        contents = [["S", "T", "V", "V"],
                    ["V", "V", "V", "X"],
                    ["V", "Z", "V", "Y"],
                    ["Y", "Z", "V", "Y"]]

        game.create_contents(contents)

        initial = game._game_state[0][2]

        matches = game.check_all_sides(initial)

        initial = [game._game_state[1][1],
                   game._game_state[2][0],
                   game._game_state[1][2],
                   game._game_state[2][2],
                   game._game_state[3][2]]

        self.assertEqual(matches, initial)

    def test_update_match_gems(self):
        game = ColumnsGame((4,4))
        contents = [["S", "T", "V", "V"],
                    ["V", "V", "V", "X"],
                    ["V", "Z", "V", "Y"],
                    ["Y", "Z", "V", "Y"]]

        game.create_contents(contents)

        list_of_cells = []
        for num in range(10):
            gem = Gem("W")
            cell = Cell(Location(0,0))
            cell.add_content(gem)
            list_of_cells.append(cell)

        game._update_matching_gems(list_of_cells)

        for cell in list_of_cells:
            gem = cell.peek_content()
            self.assertEqual(gem.get_state(), GemState.MATCH)

    def test_consecutive_drops(self):
        game = ColumnsGame((4,4))
        contents = [[" ", " ", " ", " "],
                    ["V", " ", " ", "X"],
                    ["V", "X", " ", "Y"],
                    ["Y", "Z", "V", "Y"]]

        game.create_contents(contents)
        game._create_faller("S", "T", "V")
        self.assertEqual(game.drop_in_faller(Location(0,1), 2), True)
        formated_game_field = game.get_formated_game_state()
        for line in formated_game_field:
            print(line)
        game.drop_faller_once()
        self.assertEqual(game.drop_in_faller(Location(0,1), 1), True)
        formated_game_field = game.get_formated_game_state()
        for line in formated_game_field:
            print(line)
        self.assertEqual(game.drop_in_faller(Location(0,1), 0), False)
        

if __name__ == '__main__':
    unittest.main()
        
