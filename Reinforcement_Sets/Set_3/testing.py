#Testing file
from collections import namedtuple
import problem2

Person = namedtuple('Person', ['name', 'age', 'favorite'])
instructor = Person(name = 'Alex', age = 47, favorite = 'Boo')
x = problem2.pretty_print(instructor)
