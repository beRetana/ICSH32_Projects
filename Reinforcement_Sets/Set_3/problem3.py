from collections import namedtuple
from pathlib import Path

def build_grade_report(path:'Path', ranges: dict[str:int])-> dict[str:'namedTuple']:
    'Takes a path to a text file with grades for students and returns a dictionary with that summarized data'

    file = read_line_file(path)

    Student = namedtuple('Student', ['scores', 'grade'])

    grade_report = {}

    for line in file:
        student_information = _extract_data(line)
        letter_grade = ""
        total_score = 0

        for score in student_information[1]:
            total_score += score

        if len(ranges) < 1:
            continue
        
        for letter_range in ranges:
            bounds = ranges[letter_range]
            if len(bounds)< 2:
                if (bounds[0] < total_score):
                    letter_grade = letter_range
                    break
            else:
                if(bounds[0] <= total_score < bounds[1]):
                    letter_grade = letter_range
                    break     

        grade_report[student_information[0]] = Student(student_information[1], letter_grade)

    return grade_report

def _extract_data(line: str)-> str and list[int]:
    'Takes a line and returns the first word and rest of items separetely'

    information = line.split()

    username = information.pop(0)

    information_float = []

    for grade in information:
        grade = _check_float(grade)
        if grade == None:
            continue
        information_float.append(grade)

    return username, information_float

def _check_float(value: str)-> float | None:
    'Attempts to convert a str to a foat'
    float_value = 0
    try:
        float_value = float(value)
    except:
        return None

    return float_value
    
def _read_line_file(path:'Path') -> list[str]:
    'Returns a list containing the lines of a txt document'

    file = []
    
    try:
        file_read = path.open('r')
        while (True):
            file_line = file_read.readline()
            if(file_line == ""):
                break
            else:
                if(_check_line(file_line[:-1])):
                    file.append(file_line[:-1])
    finally:
        file_read.close()

    return file

def _check_line(line: str) -> bool:
    'Checks if the line is valid'
    spaces = " "
    tabs = "\t"
    comment = "#"
    
    if(line == "\n" or _check_key(line, spaces, tabs)):
        return False
    if(line.find(comment) > -1):
        if(_check_key(line[:line.find(comment)], spaces, tabs)):
            return False
    return True

def _check_key(line: str, key: str, key_two) -> bool:
    'Checks if any character that is not key or not key_two is in line'
    for char in line:
        if(char != key and char != key_two):
            return False

    return True

if __name__ == "__main__":
    assert _check_line("#Comments should not be valid") == False
    assert _check_line("Regular lines should be valid") == True
    assert _extract_data("username 30 59 34 32 24 45656 233") == ("username", [30.0,59.0,34.0,32.0,24.0,45656.0,233.0])
    assert _extract_data("30004") == ("30004", [])
    assert _extract_data("username 30 lol str 233") == ("username", [30.0,233.0])
    
