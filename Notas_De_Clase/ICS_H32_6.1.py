# ICS H32 Week 6 Lecture 1

# In python you can store any type in a variable, even if you place in new types into those variables.

# The varible x starts off by being an int
x = 3

# Not it's a tuple
x = (1,2)

# How do you use anything if you don't know what anything is?

# Part of the answer is "vigilance".

w  = "Alex"

q = 57

len(w)

# Cannot ask len(q)

# Python resolves types at run time.
# Python documentation colloquially refers to this as "duck typing".

# "If a bird walks like a duck and quacks like a duck, it's a duck."


class ZeroLength:
    def __len__(self):
        return 0

z = ZeroLength()
len(z)


s = "Hello"
s.upper()

def double_upper(x):
    return x.upper() + x.upper()

double_upper("CHANCY")

class XYZ:
    def upper(self):
        return "Argh!"

double_upper(XYZ())

class Abc:
    def upper(self):
        return 13

double_upper(Abc())

# Python's "duck typing" is a feature we can use for good or for evil.

list([1,2,3])

list((1,3,4))

list({1,2,3,4})

list(range(5))

list('BOO')



for x in [1,2,3]:
    print(x)

for x in (1,2,3):
    print(x)

for x in {1,2,3}:
    print(x)

for x in range(4):
    print(x)

for x in "Boo":
    print(x)


# Lists, ranges, strings, sets, and a lot more types
# are _iterable_.

# Let's wirte a function just like the built-in list() function and
# see how difficult it is...

def makelist(items):
    the_list = []

    for x in items:
        the_list.append(x)

    return the_list

makelist([1,2,4])

makelist({"a", "b"})

makelist(range(5))

makelist("Boo")

# makelist(18) wouldn't work because it is not iterable




# Suppose that I want to write lots of classes that each have the ability
# to perform some calculations given a single input.

# We'll say object of those classes are _calcs_.

# Let's define an _inteface for cals.

# def calculate(self, n)
#   Takes the input n, performs the appropiate calculation, and
#   gives a result.


class ZeroCalc:
    def zero_out(self, n):
        return 0

class FirstSquareCalc:
    def square(self, n):
        return n * n

class CubeCalc:
    def calculate(self, n):
        return n * n * n


def duplicate_calc(c: 'Calc', n):
    return c.calculate(c.calculate(n))

duplicate_calc(SquareCalc(), 2)


duplicate_calc(CubeCalc(), 2)


class SquareCalc:
    def calculate(self, n):
        return n * n


def run_calcs(calcs: list['Calc'], starting_value):
    current_value = starting_value

    for clac in calcs:
        current_value = calc.calculate(current_value)

    return current_value

# What do I want to be able to say?

# run_calcs([SquareCalc()], MultipleByCalc(4), 5)


class MultipleByCalc:

    def __init__(self, mulitiplier):
        self._mulitiplier = multiplier

        
    def calculate(self, n):
        return n * self._multiplier
        

run_calcs([SquareCalc()], MultipleByCalc(4), 5)























    
