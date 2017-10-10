# Introducción
Esta librería permite obtener información meteorológica actual de un lugar o una ciudad usando la API que provee
OpenWeatherMap.
Para más información sobre OpenWeatherMap, visitar la página https://openweathermap.org

Para empezar a utilizar pyweather, debes crear una clave API en la página oficial.
En función de que cuenta hayas creado, tendrás acceso o no a determinados endpoints de la API de OpenWeatherMap:
- La información meteorológica actual de una ciudad o lugar pueden consultarse con cualquier tipo de cuenta, aunque la versión
"free" solo permite un máximo de 60 peticiones por minuto.

- La información meteorológica historica de una ciudad o lugar no puede consultarse con una cuenta "free". Debes contar con
una cuenta "starter", "medium" o "advanced"
Para más información, ver https://openweathermap.org/price

# Ejemplos
Utilizar pyweather es sencillo. Basta con ver un par de ejemplos para familiarizarse con la librería:

El siguiente ejemplo muestra información del tiempo actual de Olite, España: http://www.openstreetmap.org/?mlong=-1.64323&mlat=42.816872#map=12/42.4451/-1.6794

```
from pyweather.provider import *
from pyweather.cities import *

# Search my city
my_city = City.get_by_name(name = 'Olite', country = 'es')

# Get current weather time
provider = Provider(api_key = '{your api key here}')
weather = provider.get_current_weather(city = my_city)

# Print weather time info
print(str(weather))
```

Para consultar la información del tiempo de un lugar cuyas coordenadas son "{long}, {lat}"...

```
from pyweather.provider import *
from pyweather.cities import *

# Search my city
somewhere = ({long}, {lat})

# Get current weather time
provider = Provider(api_key = '{your api key here}')
weather = provider.get_current_weather(coords = somewhere)

# Print weather time info
print(str(weather))
```

Por último, si queremos ver el historial de información meteorológica de Madrid en el último año (obteniendo información
del tiempo cada dos días)...
```
from pyweather.provider import *
from pyweather.cities import *
from datetime import datetime

madrid = City.get_by_id(id = 3117735)
print(madrid.get_name(), madrid.get_country()) # Madrid, ES

provider = Provider(api_key = '{your api key here}')
weathers = provider.get_weather_history(city=my_city, start=datetime(year = 2016, month = 1, day = 1),
                                       end=datetime(year = 2016, month = 12, day = 31),
                                       interval = 2)
for weather in weathers:
  print('Weather in Madrid on {}: {}'.format(weather.get_timestamp(), str(weather)))
```
