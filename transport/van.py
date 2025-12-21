from .vehicle import Vehicle

class Van(Vehicle):
    def __init__(self, capacity, is_refrigerated):
        super().__init__(capacity)
        self.is_refrigerated = self._validate_fridge(is_refrigerated)

    def _validate_fridge(self, value):
        if not isinstance(value, bool):
            raise ValueError("Флаг холодильника должен быть True или False")
        return value

    def __str__(self):
        fridge_status = "с холодильником" if self.is_refrigerated else "без холодильника"
        return f"Фургон {fridge_status} | {super().__str__()}"