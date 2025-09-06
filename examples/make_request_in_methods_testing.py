from functools import wraps
from zmq_requests import make_request_decorator

'''
    Still testing
'''

def get_instance_from_method(method: callable):

    @wraps(method)
    def wrapper(*args, **kwargs):
        return args[0]
    
    return wrapper

def make_service_request(method: callable) -> callable:

    instance = get_instance_from_method(method)
    socket = instance.socket

    return make_request_decorator(
        lambda var: socket.send_string(var),
        lambda: socket.recv_string())