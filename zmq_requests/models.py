import json
from dataclasses import dataclass


class RequestStatus:

    ERROR = 'ERROR'
    SUCCESS = 'SUCCESS'


@dataclass
class ServiceRequest:
    serviceName: str
    serviceArgs: dict

    def dumps(self) -> str:

        return json.dumps({'serviceName': self.serviceName, 'serviceArgs': self.serviceArgs})

@dataclass
class ServiceResponse:
    requestStatus: str
    serviceOutput: str