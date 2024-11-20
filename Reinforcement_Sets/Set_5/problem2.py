# ICS H32 Set 5 problem 2
# problem2.py 

import urllib.request
from collections import namedtuple

CommandOption = namedtuple("CommandOption", ["command_list", "level_name"])

def get_user_input(message: str)-> str:
    'Asks the user for input and returns that input'

    while True:
        user_input = input(f"{message}: ").strip()
        if user_input == "":
            print("Invalid Input Try Again!")
            continue
        else:
            return user_input
        
def get_dat_file(url: str, page_name: str)-> list[str]:
    'Makes a request to the internet and returns the contents as lines of text'

    request = urllib.request.Request(f"{url}{page_name}.dat")
    response = urllib.request.urlopen(request)
    data = response.read()
    response.close()

    str_data = data.decode(encoding = "utf-8")
    lines_data = str_data.splitlines()

    return lines_data

def extract_title(lines_data: list[str])->str:
    'Gets the title/name of the location and returns it'

    for line in lines_data:
        if "TITLE" in line:
            return line[6:]
        
    return "NOT FOUND" 

def extract_content(start_content: str, end_content: str, lines_data: list[str])->str:
    'Gets the lines in between a starting line and an ending line'

    in_content = False

    content_lines = []

    for line in lines_data:
        if end_content in line:
            return content_lines
        if in_content:
            content_lines.append(line)
            continue
        elif start_content in line:
            in_content = True
            continue
        
    return "NOT FOUND"

def extract_description(lines_data: list[str])->list[str]:
    'Gets the lines that include the description of the location'

    return extract_content("DESCRIPTION", "END DESCRIPTION", lines_data)
    
def extract_command_options(lines_data: list[str])->list[CommandOption]:
    'Extract lines for commands and returns a list with all the possible commands'

    command_lines = extract_content("COMMANDS", "END COMMANDS", lines_data)

    if command_lines == "NOT FOUND":
        return "NOT FOUND"
    
    commands_list = []

    for line in command_lines:
        commands, level_name = line.split(sep=":")
        commands = commands.split(sep=",")
        commands_list.append(CommandOption(commands, level_name))
    
    return commands_list

def valid_command(commands_list:list[CommandOption])-> str:
    'Checks if the commands inputed are a viable option'

    while True:
        user_command = get_user_input("INSERT COMMAND").strip().lower()

        for command in commands_list:
            for command_options in command.command_list:
                if user_command in command_options.lower():
                    return command.level_name

def run_game()->None:
    'Runs the gameloop of the game'

    level_name = "start"

    progress = []

    url = get_user_input("Please Enter URL")
    print()

    while True:

        data_lines = get_dat_file(url, level_name)

        title = extract_title(data_lines)

        print(title)
        print()

        if not title in progress:

            description = extract_description(data_lines)

            print("DESCRIPTION:")

            for line in description:
                print(line)

            print()

        if "GAME OVER" in data_lines[-1]:
            print("GAME OVER")
            return

        commands = extract_command_options(data_lines)

        level_name = valid_command(commands)

        progress.append(title)
        print()
        
if __name__ == "__main__":
    run_game()
    


    
