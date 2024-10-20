
def first_chars(words: 'List of string') -> str:

    combined = ""

    try:
        if words == None or words == []:
            return combined
    
        for item in words:
            if(item == "" or item == None):
                continue
            if type(item) == str:
                combined += item[0]
            elif type(item) == list:
                combined += first_chars(item)
            else:
                continue
        
    except TypeError:
        print("Wrong parameter type")
    
    return combined

def count_bigger(objects: 'List of objects', threshold: int | float) -> int:

    count = 0;

    try:
        if objects == None or objects == []:
            return count

        for item in objects:
            if type(item) == int or type(item) == float:
                if(item > threshold):
                    count += 1
            elif type(item) == list:
                count += count_bigger(item, threshold)
            else:
                continue

    except TypeError:
        print("Wrong parameter types")

    return count



if(__name__ == "__main__"):
    assert first_chars(['Boo', 'is', 'happy', 'today']) == 'Biht'
    assert first_chars(['boo', 'was', ['sleeping', 'deeply'], 'that', 'night', ['as', ['usual']]]) == 'bwsdtnau'
    assert first_chars(['n', '', ['sleeping', 'deeply'], 'that',[[[[[[["s"]]]]]]], 'night', ['as', ['']]]) == 'nsdtsna'
    assert count_bigger([1, 2, 3, 4, 5, 6], 2.5) == 4
    assert count_bigger(['boo', [3.0, 'is', 'perfect'], 'today', 5, []], 3) == 1
