from pathlib import Path
import json
import sys

class JsonFile:

    def __init__(self, file_name:str):
        path = Path(file_name.replace('\u200b', ''))
        self.name = file_name
        if not path.exists():
            print("FAILED")
            print(file_name)
            print("MISSING")
            sys.exit()
        file = path.open('r')
        
        self._json_data = json.load(file)

    def get_json_file(self)-> json:
        'returns the json file stored in the object'

        return self._json_data

    def get_data_property(self, data_requested: str) -> json:
        'returns a certain part of the json file'
        
        try:
            self._json_data[data_requested]
        except:
            print("FAILED")
            print(self.name)
            print("FORMAT")
            sys.exit()
        
        return self._json_data[data_requested]