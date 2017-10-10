
import logging

class Logger:
    '''
    Esta clase permite generar logs para depurar el código y las requests
    de esta librería
    Esta clase usa el patrón singleton.
    '''
    class _Logger:
        def __init__(self):
            self.handler = logging.getLogger(__name__)

        def __getattr__(self, item):
            return getattr(self.handler, item)


    instance = None
    def __init__(self):
        if Logger.instance is None:
            Logger.instance = Logger._Logger()

    def __getattr__(self, item):
        return getattr(Logger.instance, item)



logger = Logger()
