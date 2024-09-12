import orjson
from typing import Callable, TypeVar

T = TypeVar("T")

class Deserializers:

    deserialization_functions = {
        int: lambda val_str: int(val_str),
        float: lambda val_str: float(val_str),
        str: lambda val_str: val_str,
        list: lambda val_str: orjson.loads(val_str),
        dict: lambda val_str: orjson.loads(val_str),
        None: lambda val_str: None
        }

    @classmethod
    def get(cls, to_type: T) -> Callable[[str], T]:
        return cls.deserialization_functions.get(to_type)
    
    @classmethod
    def __get__(cls, to_type: T) -> Callable[[str], T]:
        return cls.get(to_type)
    
    @classmethod
    def add_deserializer(cls, to_type: T, function: Callable[[str], T]) -> None:
        cls.deserialization_functions.update({to_type: function})
    
    @classmethod
    def deserialize(cls, value: str, to_type: T) -> T:

        deserializer = cls.get(to_type)
        
        return deserializer(value)


