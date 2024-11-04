from pathlib import Path

# lol

def check_line(line: str) -> bool:
    'Checks if the line is valid to be counted'
    spaces = " "
    tabs = "\t"
    comment = "#"
    
    if(line == "\n" or check_key(line, spaces, tabs)):
        return False
    if(line.find(comment) > -1):
        if(check_key(line[:line.find(comment)], spaces, tabs)):
            return False
    return True

def check_key(line: str, key: str, key_two) -> bool:
    'Checks if any character that is not key or not key_two is in line'
    for char in line:
        if(char != key and char != key_two):
            return False

    return True

def lines_of_code(path):
    num = 0;
    
    try:
        path = path.open('r')

        while (True):
            line = path.readline()
            if(line == ""):
                break
            else:
                if(check_line(line[:-1])):
                    num = num + 1
                    
    except ValueError:
        print("Wrong File type")
        
    except:
        print("Some Unknown Error Happened")
        
    finally:
        path.close()

    return num
