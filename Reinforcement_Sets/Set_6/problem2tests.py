# problem2tests.py

import unittest
import problem2


class ProblemTwoTests(unittest.TestCase):

    def test_transpose_a_two_by_two_list(self):

        list1 = [[1,2],[1,2]]

        list2 = problem2.reverse_transpose(list1)
        
        self.assertListEqual([[2,2],[1,1]], list2)

        pass

    def test_getting_a_list_with_the_last_items_in_the_inner_lists(self):

        list1 = [[1, 2, 3],[1, 2, 3]]

        list2 = problem2._get_column_items(list1, 2)
        
        self.assertListEqual([3,3], list2)

    def test_assignment_example(self):
        
        a = [['x', 'y', 'z'], ['w', 'v', 't'], ['p', 'r', 's']]
        
        b = problem2.reverse_transpose(a)

        c = [['s', 't', 'z'], ['r', 'v', 'y'], ['p', 'w', 'x']]

        self.assertListEqual(c, b)

    def test_reverse_a_list(self):

        a = ['x', 'y', 'z']
        
        b = problem2._reverse_list(a)

        c = ['z', 'y', 'x']

        self.assertListEqual(c, b)

    def test_adding_up_numbers(self):

        c = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

        d = problem2._get_sums(c, 0,0)

        self.assertEqual(45, d)


    def test_calculate_sums(self):

        c = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

        problem2.calculate_sums(c)

        b = [[45, 33, 18], [39, 28, 15], [24, 17, 9]]

        self.assertListEqual(c, b)


    def test_calculate_sums_two(self):

        c = [[1, 2], [1, 3], [7, 8]]

        problem2.calculate_sums(c)

        b = [[22, 13], [19, 11], [15, 8]]

        self.assertListEqual(c, b)

        
if __name__ == '__main__':
    unittest.main()
