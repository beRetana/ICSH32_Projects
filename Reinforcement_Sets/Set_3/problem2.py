from collections import namedtuple


def pretty_print(named_tuple: 'namedtuple')-> str:
    'Finds the longest field in a named tupple and format the printing based on that'

    max_length = 0
    
    for field in named_tuple._fields:
        if len(field) >= max_length:
            max_length = len(field)

    space = " "

    answer = ""

    for num in range(len(named_tuple)):
        mulitiplier = max_length - len(named_tuple._fields[num])
        answer += f"{space * mulitiplier}{named_tuple._fields[num]}: {named_tuple[num]}\n"

    answer = answer[:-1]
    print(answer)

    if __name__ == "__main__":
        return answer

if __name__ == "__main__":
    Person = namedtuple('Person', ['name', 'age', 'favorite'])
    instructor = Person(name = 'Alex', age = 47, favorite = 'Boo')
    assert pretty_print(instructor) == f"    name: Alex\n     age: 47\nfavorite: Boo"
    Point = namedtuple('Point', ['x', 'y', 'z'])
    pt = Point(z = 5, x = 9, y = 13)
    assert pretty_print(pt) == f"x: 9\ny: 13\nz: 5"
    Point1 = namedtuple('Point1', ['Math', 'English', 'Science'])
    pt1 = Point1(98,37,23033)
    assert pretty_print(pt1) == f"   Math: 98\nEnglish: 37\nScience: 23033"
    test = namedtuple('Test', ['Testing', 'HelloWorld', 'GoodBye'])
    test1 = test("Testing Lenghts", True, 9376)
    assert pretty_print(test1) == f"   Testing: Testing Lenghts\nHelloWorld: True\n   GoodBye: 9376"
