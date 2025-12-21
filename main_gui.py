import dearpygui.dearpygui as dpg
import os
import json
import re

from transport.client import Client
from transport.van import Van
from transport.ship import Ship
from transport.company import TransportCompany

company = TransportCompany("ГрузЭкспресс")

dpg.create_context()

with dpg.font_registry():
    with dpg.font(r"C:\Windows\Fonts\arial.ttf", 18, default_font=True, tag="DefaultFont") as f:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
dpg.bind_font("DefaultFont")

def show_error(title, message):
    if dpg.does_item_exist("err_win"):
        dpg.delete_item("err_win")
    with dpg.window(label=title, modal=True, tag="err_win", pos=(350, 200)):
        dpg.add_text(message)
        dpg.add_button(label="Ок", width=75, callback=lambda: dpg.delete_item("err_win"))

def update_tables():
    dpg.delete_item("clients_tbl", children_only=True)
    dpg.delete_item("vehicles_tbl", children_only=True)

    dpg.add_table_column(label="Имя", parent="clients_tbl")
    dpg.add_table_column(label="Вес (т)", parent="clients_tbl")
    dpg.add_table_column(label="VIP", parent="clients_tbl")

    for c in company.clients:
        with dpg.table_row(parent="clients_tbl"):
            dpg.add_text(c.name)
            dpg.add_text(f"{c.cargo_weight}")
            dpg.add_text("Да" if c.is_vip else "Нет")

    dpg.add_table_column(label="ID", parent="vehicles_tbl")
    dpg.add_table_column(label="Тип", parent="vehicles_tbl")
    dpg.add_table_column(label="Г/П (т)", parent="vehicles_tbl")
    dpg.add_table_column(label="Загрузка", parent="vehicles_tbl")

    for v in company.vehicles:
        v_type = "Фургон" if isinstance(v, Van) else "Судно"
        with dpg.table_row(parent="vehicles_tbl"):
            dpg.add_text(v.vehicle_id[:8])
            dpg.add_text(v_type)
            dpg.add_text(f"{v.capacity}")
            dpg.add_text(f"{v.current_load:.2f}")

def add_client_cb():
    name = dpg.get_value("c_name").strip()
    weight_str = dpg.get_value("c_weight")
    is_vip = dpg.get_value("c_vip")

    if not re.match(r"^[A-Za-zА-Яа-яЁё\s]{2,}$", name):
        show_error("Ошибка ввода", "Имя должно содержать только буквы (мин. 2)")
        return

    try:
        weight = float(weight_str)
        if weight <= 0 or weight > 10000: raise ValueError
    except ValueError:
        show_error("Ошибка ввода", "Вес должен быть числом от 0.1 до 10000")
        return

    company.add_client(Client(name, weight, is_vip))
    update_tables()
    dpg.set_value("status_txt", f"Клиент {name} добавлен")
    dpg.hide_item("add_client_win")
    dpg.set_value("c_name", "")
    dpg.set_value("c_weight", "")

def add_vehicle_cb():
    v_type = dpg.get_value("v_type_select")
    cap_str = dpg.get_value("v_capacity")
    
    try:
        capacity = float(cap_str)
        if capacity <= 0: raise ValueError
    except ValueError:
        show_error("Ошибка", "Грузоподъемность должна быть больше 0")
        return

    if v_type == "Фургон":
        has_fridge = dpg.get_value("v_van_fridge")
        new_v = Van(capacity, has_fridge)
    else:
        s_name = dpg.get_value("v_ship_name").strip()
        if not s_name:
            show_error("Ошибка", "Введите название судна")
            return
        new_v = Ship(capacity, s_name)

    company.add_vehicle(new_v)
    update_tables()
    dpg.set_value("status_txt", "Транспорт добавлен")
    dpg.hide_item("add_v_win")
    dpg.set_value("v_capacity", "")
    dpg.set_value("v_ship_name", "")

def save_to_file():
    if not company.clients:
        show_error("Экспорт", "Нет данных для сохранения")
        return
    output = {
        "clients": [{"name": c.name, "weight": c.cargo_weight, "vip": c.is_vip} for c in company.clients],
        "vehicles": [{"id": v.vehicle_id, "load": v.current_load} for v in company.vehicles]
    }
    if not os.path.exists("data"): os.mkdir("data")
    with open("data/result.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    dpg.set_value("status_txt", "Результат сохранен в data/result.json")

def run_distribution():
    if not company.clients or not company.vehicles:
        show_error("Ошибка", "Добавьте хотя бы одного клиента и транспорт")
        return
    company.optimize_cargo_distribution()
    update_tables()
    dpg.set_value("status_txt", "Грузы успешно распределены")

with dpg.window(tag="Primary Window"):
    with dpg.menu_bar():
        with dpg.menu(label="Файл"):
            dpg.add_menu_item(label="Экспорт", callback=save_to_file)
        with dpg.menu(label="Справка"):
            dpg.add_menu_item(label="О программе", callback=lambda: dpg.show_item("about_win"))

    with dpg.group(horizontal=True):
        dpg.add_button(label="Добавить клиента", callback=lambda: dpg.show_item("add_client_win"))
        dpg.add_button(label="Добавить транспорт", callback=lambda: dpg.show_item("add_v_win"))
        dpg.add_button(label="Распределить грузы", callback=run_distribution)

    with dpg.group(horizontal=True):
        with dpg.child_window(width=400, height=400):
            dpg.add_text("Клиенты", color=[100, 200, 255])
            with dpg.table(tag="clients_tbl", header_row=True, borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True):
                dpg.add_table_column(label="Имя")
                dpg.add_table_column(label="Вес (т)")
                dpg.add_table_column(label="VIP")

        with dpg.child_window(width=570, height=400):
            dpg.add_text("Транспорт", color=[100, 200, 255])
            with dpg.table(tag="vehicles_tbl", header_row=True, borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True):
                dpg.add_table_column(label="ID")
                dpg.add_table_column(label="Тип")
                dpg.add_table_column(label="Г/П (т)")
                dpg.add_table_column(label="Загрузка")

    with dpg.group(horizontal=True):
        dpg.add_text("Статус:")
        dpg.add_text("Готов к работе", tag="status_txt", color=[0, 255, 0])

with dpg.window(label="Добавление клиента", modal=True, show=False, tag="add_client_win", width=300, no_resize=True):
    dpg.add_input_text(label="Имя", tag="c_name")
    dpg.add_input_text(label="Вес", tag="c_weight")
    dpg.add_checkbox(label="VIP клиент", tag="c_vip")
    dpg.add_button(label="Добавить", width=-1, callback=add_client_cb)

with dpg.window(label="Добавление транспорта", modal=True, show=False, tag="add_v_win", width=350, no_resize=True):
    dpg.add_combo(["Фургон", "Судно"], label="Тип", tag="v_type_select", default_value="Фургон", 
                  callback=lambda: (dpg.configure_item("van_props", show=(dpg.get_value("v_type_select") == "Фургон")), 
                                    dpg.configure_item("ship_props", show=(dpg.get_value("v_type_select") == "Судно"))))
    dpg.add_input_text(label="Грузоподъемность", tag="v_capacity")
    with dpg.group(tag="van_props"):
        dpg.add_checkbox(label="Холодильник", tag="v_van_fridge")
    with dpg.group(tag="ship_props", show=False):
        dpg.add_input_text(label="Название судна", tag="v_ship_name")
    dpg.add_spacer(height=10)
    dpg.add_button(label="Подтвердить", width=-1, callback=add_vehicle_cb)

with dpg.window(label="О программе", modal=True, show=False, tag="about_win", pos=(300, 200)):
    dpg.add_text("Лабораторная работа 13")
    dpg.add_text("Вариант: 3")
    dpg.add_text("Разработчик: Мигунов Матвей")
    dpg.add_separator()
    dpg.add_button(label="Закрыть", width=-1, callback=lambda: dpg.hide_item("about_win"))

dpg.create_viewport(title='Транспортная Логистика | GUI', width=1000, height=550)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()