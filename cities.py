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
'''
Este script provee utilidades para obtener el información geográfica de una ciudad
específica o encontrar la ID de una ciudad por nombre
'''

from pyvalid import accepts
import sqlite3 as sqlite
from os.path import dirname, join
from logger import logger

class City:
    cities_db_path = join(dirname(__file__), 'data', 'cities.db')

    '''
    Esta clase encapsula la información geográfica de una ciudad.
    '''
    def __init__(self, id, name, country, coords):
        '''
        Constructor: Inicializa esta instancia.
        :param id: Es la id de la ciudad (es única para cada ciudad)
        :param name: El nombre de la ciudad.
        :param country: Un código de dos o tres caracteres que identifica unívocamente al
        país donde se encuentra la ciudad (no importa mayúsculas o minúsculas)
        :param coords: Es una tupla con las coordenadas de la ciudad (longitud, latitud)
        '''
        self.id = id
        self.name = name
        self.country = country.lower()
        self.longitude, self.lattitude = coords


    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_country(self):
        return self.country


    def get_coords(self):
        '''
        :return: Devuelve una tupla con las coordenadas de la ciudad (longitud, latitud)
        '''
        return self.longitude, self.lattitude

    def get_longitude(self):
        return self.longitude

    def get_lattitude(self):
        return self.lattitude



    def __str__(self):
        return '{},{}'.format(self.get_name(), self.get_country())




    @staticmethod
    @accepts(int)
    def get_by_id(id):
        '''
        Consulta la información de una ciudad por ID
        :param id: Es la ID de la ciudad.
        :return: Devuelve una instancia de la clase City con información de la ciudad cuya ID
        es la que se indica como parámetro, o None si no hay ninguna ciudad con esa ID
        '''

        try:
            query = 'SELECT id, name, country, longitude, latitude FROM cities WHERE id = ?'
            params = [id]
            result = City._sqlite_query(query, params)
            if len(result) == 0:
                return None
            data = result[0]
            id, name, country, longitude, latitude = data
            city = City(id, name, country, (longitude, latitude))
            return city
        except:
            pass
        return None


    @staticmethod
    @accepts(str, (str, None))
    def get_by_name(name, country = None):
        '''
        Consulta la información de una ciudad por nombre.
        También puede especificarse el país, para desambiguar la búsqueda.
        :param name: Es el nombre de la ciudad a buscar (no es case-sensitive)
        :param country: Si se especifica, debe ser el código del país donde buscar la ciudad
        (no es case-sensitive)
        :return: Devuelve una instancia de la clase City con información de la ciudad consultada,
        si solo hay un resultado. Si hay varios, devuelve una lista de instancias de la clase City,
        una por cada match. Si no hay ningún resultado, devuelve None
        '''

        try:
            matched_cities = []

            params = [name]
            query = 'SELECT id, name, country, longitude, latitude FROM cities WHERE name LIKE ?'
            if not country is None:
                query += ' AND country LIKE ?'
                params += [country.lower()]

            result = City._sqlite_query(query, params)
            for data in result:
                id, name, country, longitude, latitude = data
                city = City(id, name, country, (longitude, latitude))
                matched_cities.append(city)

            if not country is None:
                return matched_cities[0]

            return matched_cities if len(matched_cities) > 1 else\
                (matched_cities[0] if len(matched_cities) == 1 else None)

        except:
            pass

        return None


    @staticmethod
    def _sqlite_query(query, params):
        logger.debug('Connecting to sqlite3 database to retrieve city info...')
        with sqlite.connect(City.cities_db_path) as cities_db:
            cursor = cities_db.cursor()
            logger.debug('Executing sqlite3 query: "{}"'.format(query.replace('?', '{}').format(*params)))
            cursor.execute(query, params)
            result = cursor.fetchall()
            logger.debug('Got {} rows'.format(len(result)))

            return result