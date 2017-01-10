import time
import inspect
import functools


"""
    Print function execute state
        - Record function execute time and its arguments.
        - Print records on screen.
"""


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


"""
    Make function immortal
        - Protect function avoid crash.
"""


def immortal(function):
    def _immortal(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except:
            pass
    return _immortal


"""
    Transform function to higher-order function
        - Function can invoke with non-total mode.
"""


def higher(function):
    def _higher(*args, **kwargs):
        _new_function = functools.partial(function, *args, **kwargs)
        if set(inspect.signature(_new_function).parameters.keys()) - set(kwargs.keys()):
            return higher(_new_function)
        else:
            return _new_function()
    return _higher
