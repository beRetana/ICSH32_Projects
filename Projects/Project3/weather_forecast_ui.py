import json_connector
import api_manager
import time

def get_user_input()-> None:
    'Gets input from the user and turns it into commands and run the program'
    
    user_input_lines = []

    first_line = input()
    second_line = input()

    while True:
        user_input_queries = input().strip().split()
        if " ".join(user_input_queries) == "NO MORE QUERIES":
            break
        user_input_lines.append(user_input_queries)
    
    last_line = input()

    run(first_line, second_line, user_input_lines, last_line)

    
def run(first_line, second_line, user_input_queries, last_line)-> None:

    first_line = first_line.strip().split()
    second_line = second_line.strip().split()
    last_line = last_line.strip().split()

    if " ".join(first_line[0:2]) == "TARGET NOMINATIM":
        joined_string = " ".join(first_line[2:])
        lat, lon = api_manager.nominatim_name_to_location(joined_string)
        time.sleep(1)
    elif " ".join(first_line[0:2]) == "TARGET FILE":
        temp = json_connector.JsonFile(" ".join(first_line[2:]))
        lat = float(temp.get_json_file()[0]['lat'])
        lon = float(temp.get_json_file()[0]['lon'])

    if " ".join(second_line[0:2]) == "WEATHER NWS":
        data_holder = api_manager.get_forecast_data(joined_string)
        time.sleep(1)
    elif " ".join(second_line[0:2]) == "WEATHER FILE":
        data_holder = json_connector.JsonFile(" ".join(second_line[2:]))
        data_holder = data_holder.get_json_file()

    print(f"TARGET {right_format(lat, lon)}")

    forecast_lat, forecast_lon = api_manager.get_forcast_location(data_holder)

    print(f"FORECAST {right_format(forecast_lat, forecast_lon)}")

    if last_line[1] == "FILE":
        reverse_data_holder = json_connector.JsonFile(last_line[2])
    elif last_line[1] == "NOMINATIM":
        reverse_data_holder = api_manager.nominatim_location_to_name(forecast_lat, forecast_lon)
        time.sleep(1)

    name = reverse_data_holder.get_data_property("display_name")

    print(name)

    for query in user_input_queries:
        print(api_manager.weather_search_options(data_holder, query))

    if (" ".join(first_line[0:2]) == "TARGET NOMINATIM"):
        print("**Forward geocoding data from OpenStreetMap")
    if " ".join(second_line[0:2]) == "WEATHER NWS":
        print("**Reverse geocoding data from OpenStreetMap")
    if last_line[1] == "NOMINATIM":
        print("**Real-time weather data from National Weather Service, United States Department of Commerce")
    
def right_format(lat, lon)->str:
    'Formats coordinates to always have postives'
    if lat < 0:
        lat_str = f"{-lat}/S"
    else:
        lat_str = f"{lat}/N"
    if lon < 0:
        lon_str = f"{-lon}/W"
    else:
        lon_str = f"{lon}/E"

    return (f"{lat_str}, {lon_str}")

if __name__ == "__main__":
    queries = [["TEMPERATURE", "AIR", "C", 24, "MAX"]]
    #run("TARGET FILE nominatim_target.json​", "WEATHER FILE nws_hourly.json",queries,"REVERSE FILE nominatim_reverse.json")
    get_user_input()