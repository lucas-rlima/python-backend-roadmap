from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum 
from typing import List, Optional

class ServiceStatus(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    MAINTENANCE = "MAINTENANCE"


@dataclass
class Microservice:
    name: str
    version: str
    port: int
    status: ServiceStatus = ServiceStatus.INACTIVE
    created_at: datetime = field(default_factory=datetime.now)
    def activate(self) ->  None:
        """Ativa o microsserviço"""
        self.status =  ServiceStatus.ACTIVE

    def to_dict(self) -> dict:
        """Serializa o objeto para um dicionário"""
        return {
            "name": self.name,
            "version": self.version,
            "port": self.port,
            "status":self.status.value,
            "created_at": self.created_at.isoformat(),
        }

class EnvironmentManager:
    def __init__(self, environment_name: str) -> None:
        self.environment_name: str = environment_name
        self._services: List[Microservice] = []

    def register_service(self, service: Microservice) -> None:
        """ Add a new microservice"""
        self._services.append(service)

    def get_active_services(self) -> List[Microservice]:
        """Return only services active"""
        return [s for s in self._services if s.status == ServiceStatus.ACTIVE]

    def find_by_name(self, name: str) -> Optional[Microservice]:
        """Search a service for name. Returns None if it does not exist """
        for service in self._services:
            if service.name.lower() == name.lower():
                return service
        return None

    def decommision_service(self, name:str) -> bool:
        for service in self._services:
            if service.name.lower() == name.lower():
                return True
        return False

    # Execution black for testing
if __name__ == '__main__':
    #Instantiating the manager
    production = EnvironmentManager(environment_name="Production-Auckland")

    # Creating services instantions
    auth_service = Microservice(name="Auth-API", version="1.0.0", port=8001)
    payment_service = Microservice(name="Payment-Gateway", version="2.1.0", port=8002)

    #Changing state
    auth_service.activate()

    # Registering on 
    production.register_service(auth_service)
    production.register_service(payment_service)

    #Validation 
    print(f'Ambiente: {production.environment_name}')
    print(f'Total de serviços ativos: {len(production.get_active_services())}')

    found_service = production.find_by_name("auth-api")
    if found_service:
        print(f'Serviço Encontrado: {found_service.to_dict()}')
        