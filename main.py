import argparse
import requests
import json
import os

from datetime import datetime


def get_request(lat=54.991375, lon=73.371529, dt=0):
    weather_api_key = os.getenv("weather_api_key", default="75eeb07becc2582211e46c48eaf660e4")
    units = 'metric'
    url = f'http://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}&dt={dt}&appid={weather_api_key}&units={units}'
    response = requests.get(url)
    if not response.status_code == 200:
        raise Exception(f'HTTP response status code is not 200 \n {response.text}')
    weather = json.loads(response.text)
    return weather


def deg_to_compass(num):
    val = int((num/22.5)+.5)
    arr = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    return arr[(val % 16)]


def parse_request(json_string, units='metric') -> str:
    weather = json_string['current']
    temp = weather['temp']
    feels_like = weather['feels_like']
    pressure = weather['pressure']
    humidity = weather['humidity']
    dew_point = weather['dew_point']
    uvi = weather['uvi']
    clouds = weather['clouds']
    visibility = weather['visibility']
    wind_speed = weather['wind_speed']
    wind_deg = weather['wind_deg']
    compass_deg = deg_to_compass(wind_deg)
    weather_main = weather['weather'][0]['main']
    weather_description = weather['weather'][0]['description']

    weather_str_part_1 = f"{str(round(temp, 1)).rstrip('0').rstrip('.')}°C feels like: {str(round(feels_like, 1)).rstrip('0').rstrip('.')}°C "
    weather_str_part_2 = f"pressure: {pressure}hPa humidity: {humidity}% dew point: {str(round(dew_point,1)).rstrip('0').rstrip('.')}°C uvi: {uvi} \n"
    weather_str_part_3 = f"clouds: {clouds}% visibility: {str(visibility/1000).rstrip('0').rstrip('.')}km wind speed: {wind_speed}m/s from {compass_deg} \n"
    weather_str_part_4 = f"{weather_main},  {weather_description}"
    return weather_str_part_1 + weather_str_part_2 + weather_str_part_3 + weather_str_part_4


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--date', required=False,
        type=lambda s: datetime.strptime(s, '%Y-%m-%d %H:%M:%S'))

    parser.add_argument(
        '--lat', required=False,
        type=float
    )

    parser.add_argument(
        '--lon', required=False,
        type=float
    )

    arg_date = parser.parse_args().date

    date_time = datetime(2022, 7, 8, 20, 20, 0) if arg_date is None else arg_date  # time in local timezone
    latitude = 55 if parser.parse_args().lat is None else parser.parse_args().lat
    longitude = 73.35 if parser.parse_args().lon is None else parser.parse_args().lon

    timestamp = int(date_time.timestamp())

    json_str = get_request(dt=timestamp, lat=latitude, lon=longitude)
    weather_text = parse_request(json_str)
    print(weather_text)

    # args = parser.parse_args(['2012-01-12 20:20:00'])
    # print(args.date) # prints datetime.datetime object

