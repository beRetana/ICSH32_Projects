import json
import api_connector
import urllib.parse
import ast
from datetime import datetime, timezone, timedelta

_EMAIL = "beretana@uci.edu"
_UCI_NET_ID = "beretana"

def nominatim_name_to_location(name_location:str)-> tuple[float,float]:
    '''Creates a request to NOMINATIM to get the properties data of the location
       and returns it'''
    
    name_location = urllib.parse.quote(name_location)
    url = f"https://nominatim.openstreetmap.org/search?q={name_location}&format=json"
    header_type = "Referer"
    header_content = f"https://www.ics.uci.edu/~thornton/icsh32/ProjectGuide/Project3/{_UCI_NET_ID}"
    
    api_nominatim = api_connector.ApiConnector(url,header_type, header_content)
    macro_data = api_nominatim.get_json_file()[0]
    latitude = float(macro_data['lat'])
    longitude = float(macro_data['lon'])

    return (latitude,longitude)

def nominatim_location_to_name(lat: float, lon: float)-> str:
    'Gets coordenates and returns the location name'

    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
    header_type = "Referer"
    header_content = f"https://www.ics.uci.edu/~thornton/icsh32/ProjectGuide/Project3/{_UCI_NET_ID}"
    
    return api_connector.ApiConnector(url,header_type, header_content)

def weather_macro_request(latitude, longitude)-> api_connector.ApiConnector:
    '''Creates a request to NWS to get the properties data of the location
     and returns it as a json file'''

    url = f"https://api.weather.gov/points/{latitude},{longitude}"
    header_type = "User-Agent"
    header_content = f"(https://www.ics.uci.edu/~thornton/icsh32/ProjectGuide/Project3/, {_EMAIL})"
    
    api_weather = api_connector.ApiConnector(url, header_type, header_content)

    return api_weather

def _query_search(query_data: json, search_key_words: list[str]) -> str:
    '''Searches through the JSON file to find the data requested and return
       it as a string'''
    
    for word in search_key_words:
        try:
            query_data = query_data[word]
        except:
            return "NOT FOUND"

    return json.dumps(query_data)

def _temp_calculations(temp: float, humidity: float, wind: float)->float:
    'Calculates the feeling of the air temperature'
    
    heat_index = 0
    
    if temp >= 68:
        calculations = [-42.379]
        calculations.append(2.04901523*temp)
        calculations.append(10.14333127*humidity)
        calculations.append(-0.22475541*(temp*humidity))
        calculations.append(-0.00683783*(temp**2))
        calculations.append(-0.05481717*(humidity**2))
        calculations.append((0.00122874*humidity)*temp**2)
        calculations.append((0.00085282*temp)*humidity**2)
        calculations.append(-0.00000199*(temp**2)*(humidity**2))
        
        for num in calculations:
            heat_index += num
        
    elif temp <= 50 and wind > 3:
        calculations = [35.74]
        calculations.append(0.6215*temp)
        calculations.append(-35.75*(wind**0.16))
        calculations.append(0.4275*(temp*wind**0.16))
        
        for num in calculations:
            heat_index += num
    else:
        heat_index = temp
    
    return heat_index

def _calculate_temp_feel(json_data: json, index: int)->float|str:
    'Calculates the Temperature feels based on the formula'

    temp = float(_query_search(json_data, ['periods', index, 'temperature']))

    if temp == "NOT FOUND":
        return "NOT FOUND"
    
    temp_unit = _query_search(json_data, ['periods', index, 'temperatureUnit'])[0]
    humidity = float(_query_search(json_data, ['periods', index, 'relativeHumidity', 'value'])[0])
    wind = float(_query_search(json_data, ['periods', index, 'windSpeed']).strip('"').split()[0])

    if temp_unit == "C":
        temp = _celsius_to_fahrenheit(temp)
    
    return _temp_calculations(temp, humidity, wind) 

def _celsius_to_fahrenheit(celsius: float)->float:
    'transforms celsius to fahrenheit'
    
    return (celsius * 9/5) + 32

def _fahrenheit_to_celsius(fahrenheit: float)->float:
    'transforms fahrenheit to celsius'
    
    return (fahrenheit - 32) * 5 / 9

def _calculate_timezone(timeStamp: str) -> str:
    'Converts timestamp into UTC time'
    
    date, time = timeStamp.split(sep = "T")
    year, month, day = date.split(sep = "-")
    if time.find("-") != -1:
        time, zone = time.split(sep = "-")
        diff_hours, diff_minutes = zone.split(sep = ":")
        hours, minutes, seconds = time.split(sep = ":")
        diff_hours = -int(diff_hours) + (-int(diff_minutes)/60)
    else:
        time, zone = time.split(sep = "+")
        diff_hours, diff_minutes = zone.split(sep = ":")
        hours, minutes, seconds = time.split(sep = ":")
        diff_hours = int(diff_hours) + (int(diff_minutes)/60)

    local_time = datetime(int(year), int(month), int(day), int(hours), int(minutes), int(seconds), tzinfo=timezone(timedelta(hours=diff_hours)))
    utc_time = local_time.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    return utc_time.replace("+00:00", "Z")

def _find_min(numbers: list[tuple[float, int]])->list[tuple[float, int]]:
    'returns the smallest number in the list'
    
    num_value_index = 0
    index = 1
    min_index = numbers[0][index]
    min = numbers[0][num_value_index]

    if len(numbers) == 1:
        return (min, min_index)
    
    for number in numbers:
        if number[num_value_index] <= min:
            min = number[num_value_index]
            min_index = number[index]

    return (min, min_index)

def _find_max(numbers: list[tuple[float, int]])->list[tuple[float, int]]:
    'returns the biggest number in the list'

    num_value_index = 0
    index = 1
    max_index = numbers[0][index]
    max = numbers[0][num_value_index]

    if len(numbers) == 1:
        return (max, max_index)
    
    for number_tuple in numbers:
        if number_tuple[0] >= max:
            max = number_tuple[0]
            max_index = number_tuple[1]

    return (max, max_index)

def _get_ranged_values_base(forecast_data: json, search_query: list[str|float], length: int)-> list[tuple[float, int]]:
    'Get all the instances of data based on the query and return values and their index'
    
    list_of_values = []

    if int(length) == 0:
        value = _query_search(forecast_data['properties'], search_query)
        list_of_values.append((float(value), 0))
        return list_of_values
    
    for index in range(int(length)):
        search_query[1] = index
        value = _query_search(forecast_data['properties'], search_query)
        if value == "NOT FOUND":
            return list_of_values
        list_of_values.append((float(value), index))
    
    return list_of_values

def _get_ranged_values_temp_feels(forecast_data: json, search_query: list[str|float], length: str)-> list[tuple[float, int]]:
    'Get all the instances of data based on the query and return values and their index'
    
    list_of_values = []

    if int(length) == 0:
        value = _calculate_temp_feel(forecast_data['properties'], 0)
        list_of_values.append((value, 0))
        return list_of_values
    
    for index in range(int(length)):
        search_query[1] = index
        value = _calculate_temp_feel(forecast_data['properties'], index)
        if value == "NOT FOUND":
            return list_of_values
        list_of_values.append((value, index))
    
    return list_of_values

def _get_ranged_values_wind(forecast_data: json, search_query: list[str|float], length: int)-> list[tuple[float, int]]:
    'Get all the instances of data based on the query and return values and their index'
    
    list_of_values = []

    if int(length) == 0:
        value = float(_query_search(forecast_data['properties'], search_query).strip('"').split()[0])
        list_of_values.append((value, 0))
        return list_of_values
    
    for index in range(int(length)):
        search_query[1] = index
        value = _query_search(forecast_data['properties'], search_query)
        if value == "NOT FOUND":
            return list_of_values
        value = float(value.strip('"').split()[0])
        list_of_values.append((value, index))
    
    return list_of_values

def _temp_query_search(commands: list[str|float], forecast_data: json, search_query: list[str|float])->tuple[float, int]:
    'Searches the temperature based in query parameters and transforms the units to C or F'

    temp, type, scale, length, limit = commands
    if type == "FEELS":
        list_values = _get_ranged_values_temp_feels(forecast_data, search_query, length)

        if limit == "MAX":
            value, index = _find_max(list_values)
        else:
            value, index = _find_min(list_values)

        if scale.upper() == "C":
            value = _fahrenheit_to_celsius(value)
    else:
        
        search_query.append("temperature")
        list_values = _get_ranged_values_base(forecast_data, search_query, length)

        if limit == "MAX":
            value, index = _find_max(list_values)
        else:
            value, index = _find_min(list_values)
        search_query = ['properties','periods', index, "temperatureUnit"]
        temp_unit = _query_search(forecast_data, search_query).strip('"')
        if scale.upper() == "C":
            if temp_unit == "F":
                value = _fahrenheit_to_celsius(value)
        else:
            if temp_unit == "C":
                value = _celsius_to_fahrenheit(value)
    
    return (value, index)

def _wind_query_search(commands: list[str|float], forecast_data: json, search_query: list[str|float])->tuple[float, int]:
    
    wind, length, limit = commands
    search_query.append("windSpeed")
    list_values = _get_ranged_values_wind(forecast_data, search_query, length)
    if limit == "MAX":
        value, index= _find_max(list_values)
    else:
        value, index = _find_min(list_values)

    return (value, index)

def _base_query_search(commands: list[str|float], forecast_data: json, search_query: list[str|float])->tuple[float, int]:

    type, length, limit = commands

    list_values = _get_ranged_values_base(forecast_data, search_query, length)
    if limit == "MAX":
        value, index = _find_max(list_values)
    else:
        value, index = _find_min(list_values)

    return (value, index)

def weather_search_options(forecast_data: json , query: list[str]) -> str:
    "Returns the value of the appropiate query along it's formatting"
    
    search_query = ['periods',0]

    match query[0]:
        case "TEMPERATURE":
            value , index = _temp_query_search(query, forecast_data, search_query)
            value = f"{value:.4f}"
        case "WIND":
            value , index = _wind_query_search(query, forecast_data, search_query)
            value = f"{value:.4f}" 
        case "PRECIPITATION":
            search_query.append("probabilityOfPrecipitation")
            search_query.append("value")
            value , index = _base_query_search(query, forecast_data, search_query)
            value = f"{value:.4f}%" 
        case "HUMIDITY":
            search_query.append("relativeHumidity")
            search_query.append("value")
            value , index = _base_query_search(query, forecast_data, search_query)
            value = f"{value:.4f}%"

    time_query = ['periods', index, 'startTime']
    date_time = _query_search(forecast_data['properties'], time_query).strip('"')
    date_time = _calculate_timezone(date_time)

    return f"{date_time} {value}"
     
def get_forecast_data(name_location:str)->json:
    'Takes in a name and return the forecast data for that location'

    lat, lon = nominatim_name_to_location(name_location)
    api_weather = weather_macro_request(lat, lon)
    url = api_weather.get_data_property('properties')['forecastHourly']
    api_weather = api_weather.make_child_request(url)
    forecast_data = api_weather.get_json_file()
    return forecast_data

def get_forcast_location(data: json)->tuple[float, float]:
    'Gets the average coordinates of the place and returns those coordinates'

    query = ['geometry', 'coordinates']
    possible_locations = ast.literal_eval(_query_search(data, query))

    set_locations = set()
    for lists in possible_locations[0]:
        set_locations.add(tuple(lists))
    
    set_locations = list(set_locations)

    lat = 0
    lon = 0
    for location in set_locations:
        lat += location[1]
        lon += location[0]

    lat = lat/len(set_locations)
    lon = lon/len(set_locations)

    return (lat, lon)

def _query_testing()->None:
    'Test query cases based on Los Angeles'

    api_weather = get_forecast_data("Los Angeles")
    print(weather_search_options(api_weather, ["TEMPERATURE", "AIR", "F", 12, "MAX"]))
    print(weather_search_options(api_weather, ["TEMPERATURE", "AIR", "C", 78, "MIN"]))
    print(weather_search_options(api_weather, ["TEMPERATURE", "FEELS", "F", 10, "MAX"]))
    print(weather_search_options(api_weather, ["TEMPERATURE", "FEELS", "C", 12, "MAX"]))
    print(weather_search_options(api_weather, ["TEMPERATURE", "FEELS", "F", 0, "MAX"]))
    print(weather_search_options(api_weather, ["HUMIDITY", 12, "MAX"]))
    print(weather_search_options(api_weather, ["HUMIDITY", 45, "MIN"]))
    print(weather_search_options(api_weather, ["HUMIDITY", 0, "MIN"]))
    print(weather_search_options(api_weather, ["WIND", 12, "MAX"]))
    print(weather_search_options(api_weather, ["WIND", 0, "MIN"]))
    print(weather_search_options(api_weather, ["PRECIPITATION", 12, "MAX"]))
    print(weather_search_options(api_weather, ["PRECIPITATION", 0, "MIN"]))

def _temperature_feels_testing()->None:
    'Test Calculations'
    assert round(_temp_calculations(100, 60, 3), 7) == 129.4890272
    assert round(_temp_calculations(68, 1, 3), 7) == 65.8715397
    assert _temp_calculations(56, 1, 3) == 56
    assert _temp_calculations(50, 1, 3) == 50
    assert round(_temp_calculations(50, 1, 4), 10) == 48.8702483595

def _time_calculations_tests()->None:
    'Testing the formating of different timezones to UTC'

    assert _calculate_timezone("2024-11-12T16:00:00-08:00") == "2024-11-13T00:00:00Z"
    assert _calculate_timezone("2024-11-12T09:00:00-05:00") == "2024-11-12T14:00:00Z"
    assert _calculate_timezone("2024-11-12T21:00:00+03:00") == "2024-11-12T18:00:00Z"
    assert _calculate_timezone("2024-11-12T16:00:00-08:00") == "2024-11-13T00:00:00Z"
    assert _calculate_timezone("2024-11-12T18:00:00+01:00") == "2024-11-12T17:00:00Z"
    assert _calculate_timezone("2024-11-12T11:00:00+09:00") == "2024-11-12T02:00:00Z"

if __name__ == "__main__":
    _query_testing()
