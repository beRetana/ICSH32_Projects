# problem2.py

import math


def zero_calc(variable: 'any type')-> int:
    return 0


def square_calc(number: int|float)-> int|float:
    return number * number


def cube_calc(number: int|float)-> int|float:
    return number * number * number


def length_calc(iterable: 'iterable')-> int:
    return len(iterable)


def square_root_calc(positve_number: 'positive number')-> float:
    return math.sqrt(positve_number)


def multiply_by_calc(numbers_pair: tuple[int|float])-> int|float:
    return numbers_pair[0] * numbers_pair[1]

def convert_to_int(value: 'not an int')-> int:
    '''Takes any value and returns it as an int, or raises ErrorValue if
       not possible'''

    try:
        return int(value)
    except:
        raise ValueError

def return_function_value(f: 'function with no parameters')-> 'output of function f':
    'It returns the values returned by the function given as a parameter'

    return f()


def is_value_in_there(in_object)-> bool:

    some_value = 26
    
    return some_value in in_object

def run_calcs(calcs: list['calc functions'], starting_value):
    current_value = starting_value

    for calc in calcs:
        current_value = calc(current_value)

    return current_value
