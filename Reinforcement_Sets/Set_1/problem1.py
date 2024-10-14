    
# problem1.py
#
# ICS H32 Fall 2024
# Exercise Set 1
#
# This script asks users to specify their name and age, then,
# afterward, says "hello" to them and acknowledges how old
# they are.





    #sdkjsdnc
def run() -> None: #sdfsdc
    name = read_name()
    age = read_age()
    say_hello(name, age)

                                                                                                                                                                                                                

def say_hello(name: str, age: int) -> None:
    print(f'Hello, {name}.')
    print(f"So, I hear you're {age} {pluralize('year', 'years', age)} old.")


def pluralize(singular_word: str, plural_word: str, n: int) -> str:
    if n != 1:
        return plural_word
    else:
        return singular_word


def read_name() -> str:
    
    while(True):
        
        user_input = input('Enter your name: ')
        
        if(user_input != ""):
            break
        
        else:
            print("Input is not valid, please try again! \n")
    
    return user_input

class MyClass:


    def read_age() -> MyClass:

        while(True):

            try:
                user_input = int(input('Enter your age: '))
                break
            except ValueError:
                print("Input is not valid, please try again! \n")

        return user_input

run()
