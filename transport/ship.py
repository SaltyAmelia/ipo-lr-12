from .vehicle import Vehicle

class Ship(Vehicle):
    def __init__(self, capacity, name):
        super().__init__(capacity)
        self.name = self._validate_name(name)

    def _validate_name(self, name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Название судна должно быть непустой строкой")
        return name.strip()

    def __str__(self):
        return f"Судно '{self.name}' | {super().__str__()}"