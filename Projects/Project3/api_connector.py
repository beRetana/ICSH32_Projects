
import urllib.request
import urllib.error
import json
import sys

class ApiConnector:

    def __init__(self, url:str, header_type:str, header_content:str):
        self._header = {header_type:header_content}
        self._header_type = header_type
        self._header_content = header_content
        self._make_request(url)
        self._url = url
        
    def _make_request(self, url:str)-> None:
        'Creates a new request for the API'
        try:
            self._request = urllib.request.Request(url, headers = self._header, method = "GET")

            response = urllib.request.urlopen(self._request)
            
        except urllib.error.HTTPError as response:
            print("FAILED")
            print(f"{response.getcode()} {url}")
            if response.code != 200:
                print("NOT 200")
            else:
                print("NETWORK")
        
        else:
            data = response.read()
            response.close()
            self._json_file = json.loads(data)
        
    def make_child_request(self, url:str)-> "ApiConnector":
        'Creates a new request using previous headers'
        
        new_api_connector = ApiConnector(url, self._header_type, self._header_content)
        return new_api_connector
    
    def get_json_file(self)-> json:
        'returns the json file stored in the object'
        
        return self._json_file

    def get_data_property(self, data_requested: str) -> json:
        'returns a certain part of the json file'
        
        try:
            self._json_file[data_requested]
        except:
            print("FAILED")
            print(f"200 {self._url}")
            print("FORMAT")
            sys.exit()
        
        return self._json_file[data_requested]

