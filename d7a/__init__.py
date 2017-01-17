import jsonpickle
from enum import Enum
from tools.serialization.enum_handler import EnumHandler

jsonpickle.handlers.register(Enum, EnumHandler, base=True)