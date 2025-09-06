import orjson
from typing import Callable, TypeVar

T = TypeVar("T")

class Deserializers:
    
    """
        A utility class that provides deserialization functions for converting string
        responses into Python objects of specific types.

        This class is used inside the request-response decorator to
        automatically convert the received string response into the type specified
        in the return annotation of the decorated function.

        Attributes
        ----------
        deserialization_functions : dict
            A mapping from Python types to callables that convert a string into
            an instance of that type. Supported types:
            
            - int   : Converts the string to an integer.
            - float : Converts the string to a float.
            - str   : Returns the string unchanged.
            - list  : Parses the string as JSON and returns a list.
            - dict  : Parses the string as JSON and returns a dictionary.
            - None  : Always returns None.
    """

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
        """
            Registers a new deserialization function for a given type.

            This allows extending the `Deserializers` class to support custom
            types beyond the built-in ones (int, float, str, list, dict, None).
            The provided function should take a string as input and return an
            object of the specified type.

            Parameters
            ----------
            to_type : type
                The target Python type that the deserializer will produce.
            function : Callable[[str], T]
                A function that accepts a string and returns an instance of `to_type`.

            Returns
            -------
            None

            Examples
            --------
            >>> import numpy as np
            >>> from zmq_requests import Deserializers
            >>> Deserializers.add_deserializer(np.float64, lambda val_str: np.float64(val_str))
            >>> my_np_float64 = Deserializers[np.float64].deserialize('3.14159265359')
            ... np.float64(3.14159265359)
        """
        cls.deserialization_functions.update({to_type: function})
    
    @classmethod
    def deserialize(cls, value: str, to_type: T) -> T:
        """
            Converts a string value into the specified Python type using the
            registered deserialization function.

            This method looks up the deserializer associated with `to_type`
            in the `deserialization_functions` mapping and applies it to
            the given string.

            Parameters
            ----------
            value : str
                The string to be deserialized.
            to_type : type
                The target Python type to which the string should be converted.

            Returns
            -------
            T
                The deserialized value as an instance of `to_type`.

            Raises
            ------
            KeyError
                If no deserializer is registered for `to_type`.
            Exception
                If the deserialization function fails (e.g., invalid format).

            Examples
            --------
            >>> Deserializers.deserialize("123", int)
            123
            >>> Deserializers.deserialize("3.14", float)
            3.14
            >>> Deserializers.deserialize("[1, 2, 3]", list)
            [1, 2, 3]
            >>> Deserializers.deserialize('{"a": 1}', dict)
            {'a': 1}
        """

        deserializer = cls.get(to_type)
        
        return deserializer(value)


