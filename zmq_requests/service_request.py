import orjson
from functools import wraps
from typing import Callable, Any

from .deserialization import Deserializers
from .deserialization import T
from .models import (
    ServiceRequest,
    ServiceResponse,
    RequestStatus)


def service_request(method: Callable[[Any], T]) -> Callable[[Any], T]:
    """
        Decorator for class methods that perform request-response communication 
        over a socket-like interface.

        This decorator assumes that the decorated function belongs to a class 
        that defines a `socket` attribute. The method should return a string 
        representing the request to be sent. The decorator will:

        1. Call the decorated method and obtain the request string.
        2. Send the string through `self.socket.send_string(...)`.
        3. Wait for a reply using `self.socket.recv_string()`.
        4. Deserialize the reply into the return type specified in the method's 
        type annotation (`Note`: the type annotation must be defined).
        5. Return the deserialized response to the caller.

        Parameters
        ----------
        method : Callable
            The method being decorated. It must belong to a class that has a 
            `socket` attribute providing `send_string(str)` and `recv_string()`.

        Returns
        -------
        Callable
            A wrapped method that automatically performs request-response 
            communication using the class's `socket` attribute.

        Raises
        ------
        AttributeError
            If the instance on which the method is called does not have a 
            `socket` attribute.
        Exception
            If sending, receiving, or deserialization fails.

        Notes
        -----
        - The type annotation of the decorated method's return type is used 
        (via the `Deserializers` utility) to convert the response string 
        into the correct type.
    """
    
    @wraps(method)
    def wrapper(*args, **kwargs) -> T:
        
        method(*args, **kwargs)
        
        service_args = {
            **{arg: val for arg, val in zip(method.__code__.co_varnames[1:], args[1:])},
            **kwargs}        
        
        req_socket = args[0].socket
        req_socket.send_string(ServiceRequest(method.__name__, service_args).dumps())

        response = ServiceResponse(**orjson.loads(req_socket.recv_string()))

        if response.requestStatus != RequestStatus.SUCCESS: 
            raise Exception(f'Invalid request to service {method.__name__}. {response.serviceOutput}')
        
        return Deserializers.deserialize(response.serviceOutput, method.__annotations__['return'])
        
    return wrapper