import inspect
from singleton import singleton


class Configure:
    def __init__(self, configure: dict=None):
        self.__configure_map = {}
        if configure is not None:
            for key, value in configure.items():
                if isinstance(value, dict):
                    sub_configure = Configure(value)
                    self.__configure_map[key] = sub_configure
                else:
                    self.__configure_map[key] = value

    def __getattr__(self, item):
        if inspect.currentframe().f_back.f_code.co_name in self.__dir__():
            return object.__getattribute__(self, item)
        self.__configure_map.setdefault(item, Configure())
        return self.__configure_map[item]

    def __setattr__(self, key, value):
        if inspect.currentframe().f_back.f_code.co_name in self.__dir__():
            return object.__setattr__(self, key, value)
        self.__configure_map[key] = value


@singleton
class GlobalConfigure(Configure):
    pass