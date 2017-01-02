import time
from log import Log


def state(function):
    def _state(*args, **kwargs):
            start_time = time.time()
            function_return = function(*args, **kwargs)
            end_time = time.time()
            pass_time = end_time - start_time
            arguments = ', '.join(str(arg) for arg in args) +\
                        ', '.join('{}={}'.format(key, value) for key, value in kwargs.items())
            output = '{}({}): {}ms'.format(function.__name__, arguments, pass_time)
            print(output)
            return function_return
    return _state


def state_log(log: Log=None):
    def _state(function):
        def __state(*args, **kwargs):
            start_time = time.time()
            function_return = function(*args, **kwargs)
            end_time = time.time()
            pass_time = end_time - start_time
            arguments = ', '.join(str(arg) for arg in args) +\
                        ', '.join('{}={}'.format(key, value) for key, value in kwargs.items())
            output = '{}({}): {}ms'.format(function.__name__, arguments, pass_time)
            if log is None:
                print(output)
            else:
                log.info(output)
            return function_return
        return __state
    return _state


def immortal(function):
    def _immortal(*args, **kwargs):
        try:
            function_return = function(*args, **kwargs)
            return function_return
        except:
            pass
    return _immortal


def immortal_log(log: Log=None):
    def _immortal(function):
        def __immortal(*args, **kwargs):
            try:
                function_return = function(*args, **kwargs)
                return function_return
            except:
                if isinstance(log, Log):
                    log.exception()
        return __immortal
    return _immortal
