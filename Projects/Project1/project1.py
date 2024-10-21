from pathlib import Path
import os
import stat
import time
import shutil

def _check_path(path: str) -> bool:
    'Checks if the str is a valid path'
    try:
        path = Path(path)
        for elements in path.iterdir():
            pass
    except:
        return False
    else:
        return True

def _check_nums(nums) -> bool:
    'Checks if the str is a valid int'
    try:
        nums = int(nums)
    except:
        return False
    else:
        return True

def _take_input(options: list[str], path: bool) -> 'Tuple with required information':
    "Take user input and print ERROR if it doesn't meet format given"
    
    while True:
        user_input = input()
        for option in options:
            if len(user_input) > 2:
                if user_input[:2] == option:
                    if path:
                        if _check_path(user_input[2:]):
                            return (user_input[0], user_input[2:])
                    elif user_input[:1] == "<" or user_input[:1] == ">":
                        if _check_nums(user_input[2:]):
                            return (user_input[0], user_input[2:])
                    else:
                        return (user_input[0], user_input[2:])
            elif len(user_input) == 1:
                if user_input[0] == option:
                    return user_input[0]
            
        print("ERROR")  

def _search_files(request: tuple[str, str])-> "List of directories":
    'Search files on one directory only or and all sub-directories'

    directory_list = []
    files_list = []
    folders_list = []

    path = Path(request[1])

    for files in path.iterdir():
        if request[0] == "R" and files.is_dir():
            folders_list.append(files)
        elif not files.is_dir():
            files_list.append(files)

    file_dictionary = {}
    file_names = []
    folder_dictionary = {}
    folder_names = []

    if len(files_list) > 0:
        for path in files_list:
            file_names.append(path.name)
            file_dictionary[path.name] = path
                
        file_names.sort()
            
        for name in file_names:
            print(file_dictionary[name])
            directory_list.append(file_dictionary[name])

    if len(folders_list) > 0:
        for path in folders_list:
            folder_names.append(path.name)
            folder_dictionary[path.name] = path

        folder_names.sort()

        for name in folder_names:
            directory_list +=_search_files(("R",folder_dictionary[name]))
    
    return directory_list

def _second_search(request: tuple[str, str] | str, directories: list['Path'])-> list['Path']:
    'Filters files based on the case'

    directory_list = []

    match request[0]:
        case "A":
            return directories
        case "N":
            for files in directories:
                if (not files.is_dir() and files.name == request[1]):
                    directory_list.append(files)
            return directory_list
        case "E":
            for files in directories:
                if (not files.is_dir() and files.suffix == request[1]):
                    directory_list.append(files)
            return directory_list
        case "T":
            for files in directories:
                files_is_text = _open_file(files)
                if files_is_text != None:
                    text_file = files.read_text()
                    if request[1] in text_file:
                        directory_list.append(files)
            return directory_list
        case "<":
            for files in directories:
                if not files.is_dir() and _str_to_int(request[1]) >= 0:
                    if files.stat().st_size < int(request[1]):
                        directory_list.append(files)
            return directory_list
        case ">":
            for files in directories:
                if not files.is_dir() and _str_to_int(request[1]) >= 0:
                    if files.stat().st_size > int(request[1]):
                        directory_list.append(files)
            return directory_list

def _str_to_int(word: str) -> int:
    'Returns an int greater that 0 or equal to it if the str can be turned into one'

    size = -1
    
    try:
        size = int(word)
    finally:
        return size

def _open_file(path: 'Path') -> 'None or Path':
    'Returns the path if its a valid path and none if its not'

    path = path.open('r')
    
    try:
        path.read()
    except:
        return None
    else:
        return path

def _actions(request: str, directories: "List of directories")-> None:
    'Takes actions on files filtered based on the cases'

    directory_list = []

    match request:
        case "F":
            for files in directories:
                text = _open_file(files)
                if text != None:
                    directory_list.append(files.open('r').readline()[:-1])
                    
            if len(directory_list) == 0:
                print("NO TEXT")
            else:
                for directory in directory_list:
                    print(directory)
            return
        case "T":
            for files in directories:
                stat_result = files.stat()
                time_now = time.time()
                files.touch((time_now, time_now))
            return
        case "D":
            for files in directories:
                dup_file = files.with_suffix(files.suffix + '.dup')
                shutil.copy2(files, dup_file)
            return   

def _run_program(test_directory, test_filter, test_action) -> None:
    'Runs functions in the right sequence'

    input_options = ["D ","R "]

    #search_commands = _take_input(input_options, True)

    directories = _search_files(test_directory)
    
    if len(directories) >= 1:
        
        input_options = ["A","N ","E ","T","> ","< "]
        
        #filter_command = _take_input(input_options, False)
        
        directories = _second_search(test_filter, directories)

        for directory in directories:
            print(directory)

    if len(directories) >= 1:
        
        input_options = ["D","T","F"]
        
        #action_command = _take_input(input_options, False)
        
        directories = _actions(test_action, directories)
        

if __name__ == "__main__":
    p = "/Users/brandon__lii/Downloads/UCI/2024-2025/Fall/ICSH32/ICSH32_Work"
    input_commands = ["D ","R "]
    filter_commands = ["A","N ","E ","T","> ","< "]
    action_commands = ["D","T","F"]
    for commands in input_commands:
        for inputs in filter_commands:
            for actions in action_commands:
                if inputs == "A" or inputs == "T":
                    _run_program((elements, p), (inputs), actions)
                elif inputs == "> " or inputs == "< ":
                    _run_program((elements, p), (inputs, "10000"), actions)
                elif inputs == "N":
                    _run_program((elements, p), (inputs,"problem2.py"), actions)
                else:
                    _run_program((elements, p), (inputs,".py"), actions)
    



    
