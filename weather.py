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


class TemperatureHelper:
    '''
    Métodos auxiliares para la conversión de temperaturas en distintas escalas.
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
        str += 'Temp: {}ºC, min: {}ºC, max: {}ºC\n'.format(int(self.get_temperature()), int(self.get_min_temperature()),
                                                         int(self.get_max_temperature()))
        if self.get_clouds_level() > 0:
            str += '{}% of clouds\n'.format(int(self.get_clouds_level()))

        str += '{}% of humidity\n'.format(int(self.get_humidity()))
        str += 'Athmospheric pressure: {}hPa\n'.format(int(self.get_athmospheric_pressure()))
        str += 'Wind speed: {}m/s\n'.format(round(self.get_wind_speed(), 2))

        if self.get_rain_volume() > 0:
            str += 'Rain volume: {}mm\n'.format(round(self.get_rain_volume(), 2))

        if self.get_snow_volume() > 0:
            str += 'Snow volume: {}mm\n'.format(round(self.get_snow_volume(), 2))

        return str