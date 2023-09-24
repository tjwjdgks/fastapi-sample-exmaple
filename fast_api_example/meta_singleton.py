import os
from abc import ABCMeta


class MetaSingleton(type):
    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        if os.getenv("APPS_ENV") == "test":
            return super(MetaSingleton, cls).__call__(*args, **kwargs)

        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ABCMetaSingleton(ABCMeta):
    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        if os.getenv("APPS_ENV") == "test":
            return super(ABCMetaSingleton, cls).__call__(*args, **kwargs)

        if cls not in cls._instances:
            cls._instances[cls] = super(ABCMetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
