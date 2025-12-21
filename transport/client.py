class Client:
    def __init__(self, name, cargo_weight, is_vip=False):
        self.name = self._validate_name(name)
        self.cargo_weight = self._validate_weight(cargo_weight)
        self.is_vip = bool(is_vip)

    def _validate_name(self, name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Имя клиента должно быть текстом")
        return name.strip()

    def _validate_weight(self, weight):
        if not isinstance(weight, (int, float)) or weight <= 0:
            raise ValueError("Вес груза должен быть больше нуля")
        return float(weight)

    def __str__(self):
        status = "VIP" if self.is_vip else "Обычный"
        return f"Клиент: {self.name} | Вес: {self.cargo_weight}т | Статус: {status}"

    def __repr__(self):
        return f"Client('{self.name}', {self.cargo_weight}, {self.is_vip})"