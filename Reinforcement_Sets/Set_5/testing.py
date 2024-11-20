
import unittest
from problem2 import *

class TestPractice (unittest.TestCase):

    def test_input_with_expected_values_and_not_expected_values(self):
        #self.assertEqual(get_user_input("Input Something", ""), "")
        #self.assertEqual(get_user_input("Input Something", "Hello World"), "Hello World")
        pass

    def test_requesting_data_and_splitting_into_lines(self):
        data = 'TITLE Hallway\nDESCRIPTION\nYou are in an empty hallway, stretching in both directions, with white\nwalls, white tile floors, and white ceiling tiles.  It feels vaguely\nlike a hospital here.\n\nYou can go north or south from here.\nEND DESCRIPTION\nCOMMANDS\nN,NORTH:outside_office\nS,SOUTH:elevator\nEND COMMANDS'
        data = data.splitlines()
        url = "https://www.ics.uci.edu/~thornton/icsh32/Exercises/Set5/Ants/"
        self.assertListEqual(get_dat_file(url, "start"), data)

    def test_extract_the_right_title_from_list(self):
        line = ["Not Relevant", "TITL","TITLE HELLO WORLD!"]
        self.assertEqual(extract_title(line), "HELLO WORLD!")

    def test_extract_content_not_found(self):
        line = ["Not Relevant", "TITL","TITLE HELLO WORLD!",
                "Not Relevant", "TITLE first","DESCRIPTION",
                "Context", "Second line", "END DESCRIPTION"]
        self.assertEqual(extract_content("CONTENT", "END CONTENT", line), "NOT FOUND")
    
    def test_extract_content_found(self):
        line = ["Not Relevant", "TITL","TITLE HELLO WORLD!",
                "Not Relevant", "TITLE first","DESCRIPTION",
                "Context", "Second line", "END DESCRIPTION"]
        self.assertEqual(extract_content("TITL", "Second line", line),
                        ["TITLE HELLO WORLD!","Not Relevant",
                         "TITLE first","DESCRIPTION","Context"])

    def test_extract_description_from_list_not_found(self):
        line = ["Not Relevant", "TITL","TITLE HELLO WORLD!"]
        self.assertEqual(extract_description(line), "NOT FOUND")

    def test_extract_description_from_list(self):
        line = ["Not Relevant", "TITLE first","DESCRIPTION", "Context", "Second line", "END DESCRIPTION"]
        self.assertEqual(extract_description(line), ["Context", "Second line"])

    def test_extract_commands_options_not_found(self):
        line = ["Not Relevant", "TITL","TITLE HELLO WORLD!"]
        self.assertEqual(extract_command_options(line), "NOT FOUND")

    def test_extract_commands_options_list(self):
        line = ["COMMANDS", "N,NORTH:outside_office", "S,SOUTH:elevator", "END COMMANDS"]
        answer = [CommandOption(["N","NORTH"], "outside_office"), CommandOption(["S","SOUTH"], "elevator")]
        self.assertListEqual(extract_command_options(line), answer)

    def test_valid_commad_user_input(self):
        answer = [CommandOption(["N","NORTH"], "outside_office")]
        self.assertEqual(valid_command(answer), "outside_office")
        answer = [CommandOption(["S","SOUTH"], "elevator")]
        self.assertEqual(valid_command(answer), "elevator")


if __name__ == "__main__":
    unittest.main()