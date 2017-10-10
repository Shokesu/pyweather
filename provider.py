'''
Copyright (c) 2017 Víctor Ruiz Gómez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from datetime import datetime
from pyvalid import accepts
from pyvalid.validators import is_validator
from cities import City
from urllib.parse import urlencode
import requests
from logger import logger
from datetime import datetime
from math import floor



class TemperatureHelper:
    '''
    Métodos auxiliares para la conversión de temperatura en distintas escalas.
    '''
    @staticmethod
    def _kelvin_to_celsius(K):
        return K - 273

    @staticmethod
    def _celsius_to_fahrenheit(C):
        return 9.0 / (5.0 * C) + 32

    @staticmethod
    def _kelvin_to_fahrenheit(K):
        return TemperatureHelper._celsius_to_fahrenheit(TemperatureHelper._kelvin_to_celsius(K))

    @staticmethod
    def _kelvin_to(K, scale):
        return K if scale == 'kelvin' else \
            (TemperatureHelper._kelvin_to_celsius(K) if scale == 'celsius' else
             TemperatureHelper._kelvin_to_fahrenheit(K))


class Weather:
    '''
    Representa un conjunto de condiciones climáticas en un
    momento concreto.
    '''
    def __init__(self, data):
        '''
        Inicializa esta instancia
        :param data: Debe ser un diccionario que se obtiene como resultado de pythonizar un
        objeto JSON que se obtiene como resultado de una request a OpenWeatherMap sobre el endpoint
        /weather
        '''

        try:
            # Descripción breve del tiempo
            self.description = ', '.join([conditions_data['description'] for conditions_data in data['weather']])

            # Condiciones climatológicas.
            self.conditions = [conditions_data['main'] for conditions_data in data['weather']]

            # Presión atmosférica
            self.atmospheric_sea_pressure = float(data['main']['pressure'] if 'pressure' in data['main'] else data['main']['sea_level'])
            self.atmospheric_ground_pressure = float(data['main']['grnd_level']) if 'grnd_level' in data['main'] else None

            # Humedad
            self.humidity = float(data['main']['humidity'])

            # Temperatura
            self.temperature = float(data['main']['temp'])

            # Temperaturas mínimas y máximas
            self.min_temperature = float(data['main']['temp_min'])
            self.max_temperature = float(data['main']['temp_max'])

            # Velocidad y dirección del viento
            self.wind_speed = float(data['wind']['speed'])
            self.wind_direction = float(data['wind']['deg']) if 'deg' in data['wind'] else None

            # Nivel de nubes
            self.clouds_level = float(data['clouds']['all'])

            # LLuvia y/o viento
            self.rain_volume = float(data['rain']['3h']) if 'rain' in data else 0
            self.snow_volume = float(data['snow']['3h']) if 'snow' in data else 0

            # Timestamp
            self.timestamp = datetime.utcfromtimestamp(data['dt'])
        except:
            raise ValueError('Error parsing weather information')


    def get_timestamp(self):
        '''
        Devuelve el timestamp (instante de tiempo en el que se midió y se obtuvo estas
        condiciones climáticas)
        :return: Devuelve el timestamp (una instancia de las clase datetime.datetime en UTC)
        '''
        return self.timestamp

    def get_description(self):
        '''
        :return: Devuelve la descripción del tiempo
        '''
        return self.description

    def get_conditions(self):
        '''
        :return: Devuelve un listado con las condiciones climatológicas.
        '''
        return self.conditions


    @accepts(object, ('celsius', 'fahrenheit', 'kelvin'))
    def get_temperature(self, scale = 'celsius'):
        '''
        Consulta la temperatura.
        :param scale: Es la escala de temperaturas a usar. Posibles valores: 'celsius', 'fahrenheit', 'kelvin'
        Por defecto se usa la escala Celsius
        :return: Devuelve la temperatura en la escala indicada
        '''
        return TemperatureHelper._kelvin_to(self.temperature, scale)

    @accepts(object, ('celsius', 'fahrenheit', 'kelvin'))
    def get_min_temperature(self, scale = 'celsius'):
        '''
        Consulta la temperatura mínima.
        :param scale: Es la escala de temperaturas a usar. Posibles valores: 'celsius', 'fahrenheit', 'kelvin'
        Por defecto se usa la escala Celsius
        :return: Devuelve la temperatura en la escala indicada
        '''
        return TemperatureHelper._kelvin_to(self.min_temperature, scale)


    @accepts(object, ('celsius', 'fahrenheit', 'kelvin'))
    def get_max_temperature(self, scale = 'celsius'):
        '''
        Consulta la temperatura máxima.
        :param scale: Es la escala de temperaturas a usar. Posibles valores: 'celsius', 'fahrenheit', 'kelvin'
        Por defecto se usa la escala Celsius
        :return: Devuelve la temperatura en la escala indicada
        '''
        return TemperatureHelper._kelvin_to(self.max_temperature, scale)


    def get_humidity(self):
        '''
        Consulta el porcentaje de humedad
        :return:
        '''
        return self.humidity

    def get_clouds_level(self):
        '''
        Consulta el porcentaje de nubes
        :return:
        '''
        return self.clouds_level

    def get_athmospheric_sea_pressure(self):
        '''
        :return: Devuelve la presión atmosférica al nivel del mar en hPa
        '''
        return self.atmospheric_sea_pressure


    def get_athmospheric_ground_pressure(self):
        '''
        :return: Devuelve la presión atmosférica al nivel de la superficie en hPa
        (también puede devolver None si este valor no está disponible)
        '''
        return self.atmospheric_ground_pressure

    def get_athmospheric_pressure(self):
        '''
        Es un alias de get_athmospheric_sea_pressure
        '''
        return self.get_athmospheric_sea_pressure()

    def get_wind_speed(self):
        '''
        :return: Devuelve la velocidad del viento en metros/segundo
        '''
        return self.wind_speed

    def get_wind_direction(self):
        '''
        :return: Devuelve la dirección del viento. Puede devolver None
        (si no se posee información sobre la direción del viento)
        '''
        return self.wind_direction

    def get_rain_volume(self):
        '''
        :return: Devuelve el volumen de lluvia en las últimas 3 horas en mm
        '''
        return self.rain_volume

    def get_snow_volume(self):
        '''
        :return: Devuelve el volumen de nieve en las últimas 3 horas en mm
        '''
        return self.snow_volume

    def __str__(self):
        str = self.get_description() + '\n'
        str += 'Temp: {}ºC, min: {}ºC, max: {}ºC\n'.format(self.get_temperature(), self.get_min_temperature(),
                                                         self.get_max_temperature())
        if self.get_clouds_level() > 0:
            str += '{}% of clouds\n'.format(self.get_clouds_level())

        str += '{}% of humidity\n'.format(self.get_humidity())
        str += 'Athmospheric pressure: {}hPa\n'.format(self.get_athmospheric_pressure())
        str += 'Wind speed: {}m/s\n'.format(self.get_wind_speed())

        if self.get_rain_volume() > 0:
            str += 'Rain volume: {}mm\n'.format(self.get_rain_volume())

        if self.get_snow_volume() > 0:
            str += 'Snow volume: {}mm\n'.format(self.get_snow_volume())

        return str



class OpenWeatherMapProxy:
    class _OpenWeatherMapProxy:
        openweathermap_prefix_url = 'http://api.openweathermap.org/data/2.5'
        '''
        Esta clase se encarga de realizar requests a la API de OpenWeatherMap
        Se encarga de que dos requests iguales al endpoint 'weather' (para obtener el tiempo actual),
        no se envían en un mismo intervalo de 10 min. En dicho caso, se almacena temporalmente el resultado
        de la request en una caché, y se devuelve ese valor (hasta pasados 10 min).
        Esta clase usa el patrón Singleton
        '''
        def __init__(self):
            '''
            Inicializa la única instancia de esta clase.
            '''
            self.cache = {}

        def _get(self, query):
            # Realizamos la petición a la API
            logger.debug('Requesting data from {}'.format(query))
            response = requests.get(query)
            logger.debug('Response status code: {}'.format(response.status_code))
            logger.debug('Response headers: {}'.format(response.headers))

            # Comprobamos que la respuesta tiene estado 200
            if response.status_code != 200:
                raise Exception('Server response with {}'.format(response.status_code))

            try:
                response = response.json()
                return response
            except:
                raise Exception('Failed to decode response to JSON')

        def get(self, endpoint, params):
            '''
            Realiza una request a la API de OpenWeatherMap
            :param endpoint: Es el endpoint de la API e.g: "weather", "history/city"
            :param params: Son los parámetros de la request en forma de diccionario.
            :return: Devuelve el cuerpo de la request en formato JSON
            '''
            # Construimos la query a la API
            query = '{}/{}?{}'.format(self.openweathermap_prefix_url, endpoint, urlencode(params))

            # Si el resultado de la query está en cache, devolvemos el resultado almacenado.
            if endpoint == 'weather':
                current_time = float(datetime.utcnow().strftime('%s'))
                if (query in self.cache) and ((current_time - self.cache[query]['timestamp']) < (10 * 60)):
                    return self.cache[query]['response']
                else:
                    response = self._get(query)
                    self.cache[query] = {'response' : response, 'timestamp' : current_time}
                    return response

            return self._get(query)

    instance = None
    def __init__(self):
        if OpenWeatherMapProxy.instance is None:
            OpenWeatherMapProxy.instance = OpenWeatherMapProxy._OpenWeatherMapProxy()

    def __getattr__(self, item):
        return getattr(OpenWeatherMapProxy.instance, item)


class Provider:
    class Validator:
        '''
        Clase auxiliar para válidar algunos parámetros de los métodos de clase
        '''
        @staticmethod
        @is_validator
        def validate_coords(coords):
            return coords is None or\
                   (isinstance(coords, tuple) and len(coords) == 2 and len([coord for coord in coords if not isinstance(coord, (int, float))]) == 0)

    '''
    Esta clase es un wrapper sobre la API de OpenWeatherMap.
    Para más información sobre OpenWeatherMap, consulte la siguiente página web:
    https://openweathermap.org/
    '''
    @accepts(object, str)
    def __init__(self, api_key):
        '''
        Inicializa la instancia.
        :param api_key: Es la clave API de OpenWeatherMap
        '''
        self.api_key = api_key


    @accepts(object, (City, None), Validator.validate_coords)
    def get_current_weather(self, city = None, coords = None):
        '''
        Consulta las condiciones climáticas de una ciudad o un lugar.
        Si se especifica el parámetro "city", se consultará el tiempo actual en la ciudad
        que indica dicho parámetro.

        En caso contrario, deben especificarse las coordenadas de un lugar especifico, usando
        el parámetro "coords". Deberá ser una tupla con dos valores (latitud, longitud)

        :return: Devuelve las condiciones climáticas actuales de la ciudad o lugar indicados.
        El valor de retorno será un objeto de la clase Weather

        e.g:
        city = City.get_by_name(name = 'Olite', country = 'es')
        current_weather = PyWeather(api_key='?').get_current_weather(city)

        city = City.get_by_id(id = 6359739)
        current_weather = PyWeather(...).get_current_weather(city)
        '''

        if city is None and coords is None:
            raise ValueError('You must specify either a city or a place to get the current weather')


        # Generamos los parámetros para la request a OpenWeatherMap
        params = {}

        # Añadimos siempre la API key como parámetro
        params['APPID'] = self.api_key

        if not city is None:
            params['id'] = city.get_id()
        else:
            params['lat'], params['long'] = coords

        response = OpenWeatherMapProxy().get('weather', params)
        weather = Weather(response)
        return weather


    @accepts(object, datetime, (datetime, None), (City, None), Validator.validate_coords, (int, float))
    def get_weather_history(self, start, end = None, city = None, coords = None, interval = 1):
        '''
        Consulta el historial de condiciones climáticas de una ciudad o un lugar entre varias fechas
        que se indican como parámetro.
        Si se especifica el parámetro "city", se consultará el historial de la ciudad
        que indica dicho parámetro.
        En caso contrario, deben especificarse las coordenadas de un lugar especifico, usando
        el parámetro "coords". Deberá ser una tupla con dos valores (latitud, longitud)

        :param start: Debe ser la primera fecha (UTC) sobre la cual se consultará el tiempo de la ciudad
        o lugar. Debe ser una instancia de la clase datetime.datetime
        :param end: Deber ser la última fecha (UTC) sobre la cual se consultará el tiempo de la ciudad.
        Debe ser una instancia de la clase datetime.datetime. Si es None, por defecto será
        datetime.utcnow()
        :param interval: Indica cada cuantos días debe muestrearse el tiempo. Por ejemplo, si es 1,
        se devolverá el tiempo de cada dia entre las fechas de inicio y fin. Si es 2, cada dos dias, ...
        También puede tener un valor inferior a 1.

        :return: Devuelve una lista de instancias de la clase Weather. Cada uno de estos objetos representará
        las condiciones climáticas del lugar o ciudad indicados, en un momento específico en el tiempo.
        '''

        if city is None and coords is None:
            raise ValueError('You must specify either a city or a place to get weather history')


        # Generamos los parámetros para la request a OpenWeatherMap
        params = {}

        # Añadimos siempre la API key como parámetro
        params['APPID'] = self.api_key

        if not city is None:
            params['id'] = city.get_id()
        else:
            params['lat'], params['long'] = coords

        # Añadimos las fechas de inicioy fin y calculamos la cantidad de datos que queremos obtener.
        start = int(start.strftime('%s'))
        end = int((end if not end is None else datetime.utcnow()).strftime('%s'))
        amount = floor((end - start) / (interval * 24 * 60 * 60))

        params['start'] = start
        params['end'] = end
        params['cnt'] = amount

        response = OpenWeatherMapProxy().get('history/city', params)

        try:
            weathers = []
            for data in response['list']:
                try:
                    weather = Weather(data)
                    weathers.append(weather)
                except:
                    pass
            return weathers
        except:
            raise Exception('Error parsing weather history')