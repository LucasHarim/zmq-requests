import orjson
from dataclasses import dataclass


class RequestStatus:

    ERROR = 'ERROR'
    SUCCESS = 'SUCCESS'


@dataclass
class ServiceRequest:
    serviceName: str
    serviceArgs: dict

    def dumps(self) -> str:

        return orjson.dumps({'serviceName': self.serviceName, 'serviceArgs': self.serviceArgs}).decode("utf-8")

@dataclass
class ServiceResponse:
    requestStatus: str
    serviceOutput: str