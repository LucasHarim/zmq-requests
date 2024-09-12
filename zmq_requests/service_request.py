import orjson
from functools import wraps

from .deserialization import Deserializers
from .models import (
    ServiceRequest,
    ServiceResponse,
    RequestStatus)


def service_request(function: callable) -> callable:
    
    @wraps(function)
    def wrapper(*args, **kwargs) -> dict:
        
        function(*args, **kwargs)
        
        service_args = {
            **{arg: val for arg, val in zip(function.__code__.co_varnames[1:], args[1:])},
            **kwargs}
        
        
        req_socket = args[0].socket
        req_socket.send_string(ServiceRequest(function.__name__, service_args).dumps())

        response = ServiceResponse(**orjson.loads(req_socket.recv_string()))

        if response.requestStatus != RequestStatus.SUCCESS: 
            raise Exception(f'Invalid request to service {function.__name__}. {response.serviceOutput}')
        
        return Deserializers.deserialize(response.serviceOutput, function.__annotations__['return'])
        
    return wrapper

