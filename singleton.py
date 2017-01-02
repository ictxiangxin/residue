"""
    Singleton decorator
        - Use this decorator to make class as singleton without other modifies.
"""


def singleton(class_name):
    singleton_instances = {}

    def _singleton(*args, **kwargs):
        if class_name not in singleton_instances:
            singleton_instances[class_name] = class_name(*args, **kwargs)
        return singleton_instances[class_name]

    return _singleton
