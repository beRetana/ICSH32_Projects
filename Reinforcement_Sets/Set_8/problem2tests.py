# problem2tests.py

import unittest
from problem2 import *

class Problem2Tests(unittest.TestCase):

    def test_zero_calc_returning_zero(self):
        'Checks that regardless of the input the function returns zero'

        list_of_numbers = [-100000,-3,-1,0,1,3,100000,"", True]

        for number in list_of_numbers:
            self.assertEqual(zero_calc(number), 0)

    def test_cube_calc_returns_cubed_value_of_number_types(self):
        '''Iterates through a list of possible inputs and expects the cude of
           those values'''

        list_of_numbers = [-100000,-3,-1,0,1,3,100000]

        for number in list_of_numbers:
            self.assertEqual(cube_calc(number), number**3)

    def test_square_calc_returns_squared_value_of_number_types(self):
        '''Iterates through a list of possible inputs and expects
           to recieve the square of those values'''

        list_of_numbers = [-100000,-3,-1,0,1,3,100000]

        for number in list_of_numbers:
            self.assertEqual(square_calc(number), number**2)

    def test_square_root_calc_returns_square_rooted_value_of_number_types(self):
        '''Iterates through a list of possible inputs and expects
           to recieve the square root of those values'''

        list_of_numbers = [0,1,3,100000, .4, .999999, .23987102934, .000000001]

        for number in list_of_numbers:
            self.assertEqual(square_root_calc(number), number**0.5)


    def test_length_calc_returns_length_value_of_iterable_types(self):
        '''Iterates through a list of possible inputs and expects
           to recieve the length of those inputs'''

        list_of_iterables = ["", "Hello World", [1,2,3,4], {1:1,2:2,3:3}]

        for iterable in list_of_iterables:
            self.assertEqual(length_calc(iterable), len(iterable))

    def test_multiply_by_calc_returns_multiple_of_pair_of_numbers(self):
        '''Iterates through a list of possible inputs and expects
           to recieve the multiple of both numbers in the tuples'''

        list_of_tuples = [(1,2), (0,3), (-1,3), (-4,-6)]

        for pair in list_of_tuples:
            self.assertEqual(multiply_by_calc(pair), pair[0]*pair[1])


    def test_convert_to_int_returns_the_input_as_an_int_type(self):
        '''Iterates through a list of possible inputs and expects
           to recieve the inputs as type int'''

        list_of_valid_inputs = [1.0, -111.1111, "-1043", "022423", 13]

        for value in list_of_valid_inputs:
            self.assertEqual(convert_to_int(value), int(value))


    def test_convert_to_int_returns_value_error(self):
        '''Iterates through a list of possible inputs and expects
           to recieve a value error raised'''

        list_of_invalid_inputs = ["123m1nx23", "", "alsdncd", None, [1, 2, 3], {}, object()]

        for value in list_of_invalid_inputs:
            with self.assertRaises(ValueError):
                convert_to_int(value)


    def test_return_function_value_returns_return_value_of_function_given(self):
        '''Iterates through a list of possible inputs and expects
           to recieve the value of the function given'''

        def return_int():
            return 12

        def return_tuple():
            return ("n", 4.5)

        def return_list():
            return ["n", 4.5, [3], None]

        list_of_functions = [return_int, return_tuple, return_list]

        for function in list_of_functions:
            self.assertEqual(return_function_value(function), function())


    def test_calc_functions_that_return_numbers(self):
        '''Iterates through a list of possible inputs and expects
           to recieve the value of the input after going through all functions'''

        list_of_functions = [return_function_value, multiply_by_calc, convert_to_int,
                             square_calc, cube_calc, square_root_calc, zero_calc]

        result = 0

        def return_list():
            return [13, 2]

        self.assertEqual(run_calcs(list_of_functions, return_list), result)


    def test_is_value_in_there_that_returns_true(self):
        '''Iterates through a list of possible inputs and expects
           to recieve true'''

        list_of_values = [[26,5,2], (26, "Hello World", 23.5)]

        for value in list_of_values:
            self.assertEqual(is_value_in_there(value), True)


if __name__ == "__main__":
    unittest.main()

        
