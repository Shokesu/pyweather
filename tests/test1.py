
from provider import *
from cities import *
from logger import logger
import logging
from sys import stdout
from os.path import join, dirname

if __name__ == '__main__':
    # Enable logging to debug requests to OpenWeatherMap
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler(stdout))

    # Get your API key
    with open(join(dirname(dirname(__file__)), 'data', 'api_key.txt')) as fh:
        api_key = fh.read()

    # Search my city
    my_city = City.get_by_name(name='Olite', country='es')

    # Get current weather time
    provider = Provider(api_key)
    weather = provider.get_current_weather(city=my_city)

    # Print weather time info
    print(str(weather))