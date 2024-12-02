# problem2


def _get_column_items(original_list: list[list['objects']], index: int)-> list['objects']:
    '''Returns a new list with the items in the index position given from the inner
       lists and returns them as a new list'''

    new_list = []

    for inner_list in original_list:
        new_list.append(inner_list[index])

    return list(new_list)


def _reverse_list(original_list: list['objects'])-> list['objects']:
    '''Reverses the list and returns a new one'''

    new_list = []

    for index in range(len(original_list)-1, -1,-1):
        
        new_list.append(original_list[index])

    return new_list


def reverse_transpose(original_list: list[list['objects']])-> list[list['objects']]:

    new_list = []

    for inverse_index in range(len(original_list)-1, -1, -1):

        column = _get_column_items(original_list, inverse_index)

        new_list.append(_reverse_list(column))

    return list(new_list)


def _get_sums(original_list: list[list[float|int]], row, column)_> float|int:
    '''Gets the total of the numbers in rows and columns higher or equal to the parameters'''

    total_sum = 0

    for row_index in range(len(original_list)):

        if row_index >= row:

            for column_index in range(len(original_list[row_index])):

                if column_index >= column:

                    total_sum += original_list[row_index][column_index]
    
    return total_sum


def calculate_sums(original_list: list[list[float|int]]) -> list[list[float|int]]:

    new_list = []

    for row in range(len(original_list)):

        for column in range(len(original_list[row])):

            original_list[row][column] = _get_sums(original_list, row, column)





    



    
