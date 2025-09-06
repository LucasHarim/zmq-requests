import orjson
from functools import wraps
import inspect

from .deserialization import Deserializers
from .models import (
    ServiceRequest,
    ServiceResponse,
    RequestStatus)

from typing import Callable

def make_request_decorator(
        send_string_func: Callable[[str], None],
        recv_string_func: Callable[[], str]) -> Callable[[Callable], Callable]:
        
    """
        Creates a decorator that transforms a function into a request-response handler 
        using the provided send and receive methods.

        The decorated function will be executed, its return value converted to a string 
        and sent using `send_string_func`. After sending, the decorator waits for a 
        response using `recv_string_func` and returns that response.

        Parameters
        ----------
        send_string_func : Callable[[str], None]
            A callable that takes a string and sends it (e.g., via a socket).
        recv_string_func : Callable[[], str]
            A callable that waits for and returns a response string.

        Returns
        -------
        Callable[[Callable], Callable]
            A decorator that can be applied to functions to wrap them with request-response logic.

        Examples
        --------
        >>> def send(msg: str) -> None:
        ...     print("Sending:", msg)
        >>> def recv() -> str:
        ...     return "response"
        >>> req_decorator = make_request_decorator(send, recv)
        
        >>> @req_decorator
        ... def my_func(x, y):
        ...     return f"{x} + {y}"
        >>> result = my_func(2, 3)
        Sending: 2 + 3
        >>> print(result)
        response
    """
     
    def decorator(function: callable) -> callable:
        
        @wraps(function)
        def wrapper(*args, **kwargs) -> dict:
            
            function(*args, **kwargs)
            
            service_args = dict()
            service_args = {
                **{arg: val for arg, val in zip(function.__code__.co_varnames, args)},
                **kwargs}
            
            if inspect.ismethod(function):
                ''' 
                    Remove `self` from args
                '''
                service_args.pop('self')
            
            send_string_func(ServiceRequest(function.__name__, service_args).dumps())

            response = ServiceResponse(**orjson.loads(recv_string_func()))

            if response.requestStatus != RequestStatus.SUCCESS: 
                raise Exception(f'Invalid request to service {function.__name__}. {response.serviceOutput}')
            
            return Deserializers.deserialize(response.serviceOutput, function.__annotations__['return'])
            
        return wrapper
    
    return decorator

