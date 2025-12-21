import uuid

class Vehicle:
    def __init__(self, capacity):
        self.vehicle_id = str(uuid.uuid4())[:8]
        self.capacity = self._validate_capacity(capacity)
        self.current_load = 0.0
        self.clients_list = []

    def _validate_capacity(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Грузоподъемность должна быть положительным числом")
        return float(value)

    def load_cargo(self, client):
        from .client import Client
        if not isinstance(client, Client):
            raise TypeError("Загружать можно только объекты класса Client")
        
        if self.current_load + client.cargo_weight <= self.capacity:
            self.current_load += client.cargo_weight
            self.clients_list.append(client)
            return True
        return False

    def __str__(self):
        return (f"ID: {self.vehicle_id} | "
                f"Грузоподъемность: {self.capacity}т | "
                f"Загрузка: {self.current_load:.2f}т")