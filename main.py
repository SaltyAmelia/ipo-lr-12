from transport.client import Client
from transport.van import Van
from transport.ship import Ship
from transport.company import TransportCompany
import json

def save_to_json(company, filename="distribution_result.json"):
    data = {
        "clients": [
            {
                "name": c.name,
                "cargo_weight": c.cargo_weight,
                "is_vip": c.is_vip
            } for c in company.clients
        ],
        "vehicles": [
            {
                "vehicle_id": v.vehicle_id,
                "capacity": v.capacity,
                "current_load": v.current_load,
                "type": v.__class__.__name__,
                **({"is_refrigerated": v.is_refrigerated} if isinstance(v, Van) else {}),
                **({"name": v.name} if isinstance(v, Ship) else {})
            } for v in company.vehicles
        ]
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n[Успех] Данные сохранены в {filename}")

def main():
    company = TransportCompany("ГрузЭкспресс")

    while True:
        print("\n" + "="*50)
        print(f" СИСТЕМА УПРАВЛЕНИЯ: {company.name}")
        print("="*50)
        print("1. Добавить клиента")
        print("2. Добавить транспорт")
        print("3. Список клиентов")
        print("4. Список транспорта")
        print("5. Распределить грузы")
        print("6. Выход")
        
        choice = input("\nВыберите действие (1–6): ").strip()

        if choice == '1':
            try:
                name = input("Имя клиента: ").strip()
                weight = float(input("Вес груза (т): "))
                is_vip = input("VIP-статус? (да/нет): ").strip().lower() in ('да', 'yes', 'y', '1')
                company.add_client(Client(name, weight, is_vip))
                print(f"Клиент добавлен.")
            except Exception as e:
                print(f"Ошибка: {e}")

        elif choice == '2':
            print("\n1. Фургон (Van)\n2. Судно (Ship)")
            t_choice = input("Тип: ").strip()
            try:
                capacity = float(input("Грузоподъемность (т): "))
                if t_choice == '1':
                    fridge = input("Холодильник? (да/нет): ").strip().lower() in ('да', 'yes', 'y', '1')
                    company.add_vehicle(Van(capacity, fridge))
                elif t_choice == '2':
                    ship_name = input("Название судна: ").strip()
                    company.add_vehicle(Ship(capacity, ship_name))
                print("Транспорт добавлен.")
            except Exception as e:
                print(f"Ошибка: {e}")

        elif choice == '3':
            if not company.clients:
                print("Список клиентов пуст.")
            else:
                for i, c in enumerate(company.clients, 1):
                    print(f"{i}. {c}")

        elif choice == '4':
            if not company.vehicles:
                print("Транспорт отсутствует.")
            else:
                for i, v in enumerate(company.vehicles, 1):
                    print(f"{i}. {v}")

        elif choice == '5':
            if not company.clients or not company.vehicles:
                print("Ошибка: нужно добавить и клиентов, и транспорт.")
            else:
                company.optimize_cargo_distribution()
                print("\nРезультат распределения:")
                for v in company.vehicles:
                    print(f"\n{v}")
                    if v.clients_list:
                        for c in v.clients_list:
                            print(f"{c}")
                    else:
                        print("(пусто)")

        elif choice == '6':
            print("Завершение работы.")
            break
        else:
            print("Неверный пункт меню.")

if __name__ == "__main__":
    main()