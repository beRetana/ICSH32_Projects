#test_cell.py


import unittest
from cell import *
from gem import GemState

class TestCell(unittest.TestCase):

    def test_getting_an_empty_cell_at_creation(self):
        cell = Cell(Location(0,0))
        self.assertEqual(cell.peek_content(), "   ")

    def test_getting_cell_content_with_gem(self):
        cell = Cell(Location(0,0))
        cell.add_content(Gem("R"))
        cell.update_gem(GemState.FALLER)
        self.assertEqual(cell.peek_content().get_formated_state(), "[R]")
        cell.update_gem(GemState.FROZEN)
        self.assertEqual(cell.peek_content().get_formated_state(), " R ")
        cell.update_gem(GemState.FALLER_LANDED)
        self.assertEqual(cell.peek_content().get_formated_state(), "|R|")

    def test_pop_content(self):
        cell = Cell(Location(0,0))
        gem = Gem("T")
        gem.update_state(GemState.FROZEN)
        cell.pop_content(gem)
        self.assertEqual(cell.peek_content(), gem)
        self.assertEqual(cell.peek_content().get_formated_state(), " T ")


if __name__ == '__main__':
    unittest.main()
