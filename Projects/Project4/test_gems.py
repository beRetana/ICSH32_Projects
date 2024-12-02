# test_gems.py

# Handles all the logic to test gems

import unittest
from gem import *

class TestGems(unittest.TestCase):

    def test_getting_state_and_color_of_a_gem(self):
        gem = Gem("R")

        self.assertEqual(gem.get_color(), "R")
        self.assertEqual(gem.get_state(), GemState.EMPTY)
        gem.update_state(GemState.FALLER)
        self.assertEqual(gem.get_state(), GemState.FALLER)


if __name__ == '__main__':
    unittest.main()
