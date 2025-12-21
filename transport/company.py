from .vehicle import Vehicle
from .client import Client

class TransportCompany:
    def __init__(self, name):
        self.name = self._validate_name(name)
        self.vehicles = []
        self.clients = []

    def _validate_name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Название компании должно быть непустой строкой")
        return value.strip()

    def add_vehicle(self, vehicle):
        if not isinstance(vehicle, Vehicle):
            raise TypeError("Можно добавить только объект Vehicle или его потомка")
        self.vehicles.append(vehicle)

    def add_client(self, client):
        if not isinstance(client, Client):
            raise TypeError("Можно добавить только объект Client")
        self.clients.append(client)

    def list_vehicles(self):
        return self.vehicles

    def optimize_cargo_distribution(self):
        for v in self.vehicles:
            v.current_load = 0.0
            v.clients_list.clear()

        sorted_clients = sorted(self.clients, key=lambda c: c.is_vip, reverse=True)
        sorted_vehicles = sorted(self.vehicles, key=lambda v: v.capacity, reverse=True)

        for client in sorted_clients:
            loaded = False
            for vehicle in sorted_vehicles:
                if vehicle.load_cargo(client):
                    loaded = True
                    break
            if not loaded:
                print(f"Внимание: Груз '{client.name}' ({client.cargo_weight}т) не поместился!")