import zmq
import time
from random import randint

from zmq_requests import (
    service_request,
    Deserializers)


class ClientTest:

    def __init__(self, host: str = 'tcp://localhost', port:int = 5555, timeout_ms: int = 5000):
        
        self.host = host
        self.port = port
        self._context = zmq.Context()
        self.socket = self._context.socket(zmq.REQ)
        self.socket.connect(f'{host}:{port}')
        self.socket.RCVTIMEO = timeout_ms

        self._check_connection_with_service()
    
    def _check_connection_with_service(self) -> None:
        try: 
            self.CheckClientConnection()
        except zmq.error.Again:
            raise Exception(f'Timeout. Client cannot establish connection to server at {self.host}:{self.port}')  

    @service_request
    def CheckClientConnection(self) -> None: ...

    @service_request
    def SayHello(self) -> None: ...
    
    @service_request
    def CheckMsg(self, msg: str) -> str: ...
    
    @service_request
    def Sum(self, a: int, b: int) -> int: ...
    
    @service_request
    def Divide(self, a: float, b: float) -> float: ...
    
    @service_request
    def Add(self, a: int, b: float) -> float: ...


    @service_request
    def GetList(self) -> list: ...

    @service_request
    def GetDictionary(self) -> dict: ...

if __name__ == '__main__':

    client = ClientTest()
    
    t0 = time.time()

    for i in range(1000):
        
        client.SayHello()
        
        msg = client.CheckMsg(f'Hello from the ClientTest!')
        print(msg)

        n1 = client.Divide(1, 1) + client.Sum(i, 1.0)
        n2 = client.Sum(randint(-10, 10), randint(-10, 10))
        
        print(n1)
        print(n2)
        
        print(client.GetList())
        print(client.GetDictionary()["x"])
        
        

    delta_time = time.time() - t0
    print(f'Delta time: {round(delta_time, 3)} secs')
        