from dataclasses import dataclass
from typing import List
from random import uniform
import marshmallow_dataclass
import marshmallow
import json


@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: float


@dataclass
class Weapon:
    id: int
    name: str
    max_damage: float
    min_damage: float
    stamina_per_hit: float

    @property
    def damage(self) -> float:
        return round(uniform(self.min_damage, self.max_damage), 1)


@dataclass
class EquipmentData:
    weapons: List[Weapon]
    armors: List[Armor]


class Equipment:
    weapons: dict
    armors: dict

    def __init__(self) -> None:
        # словари с оружием и броней
        self.weapons = {}
        self.armors = {}
        # загрузка данных в словари из json
        self._load_equipment_data()

    def get_weapon(self, weapon_name: str) -> Weapon:
        # возвращает объект оружия по имени
        return self.weapons.get(weapon_name)

    def get_armor(self, armor_name: str) -> Armor:
        # возвращает объект брони по имени
        return self.armors.get(armor_name)

    def get_weapons_names(self) -> list:
        # возвращаем список с оружием
        return list(self.weapons.keys())

    def get_armors_names(self) -> list:
        # возвращаем список с броней
        return list(self.armors.keys())

    def _load_equipment_data(self):
        # загружает json в переменные weapons и armors
        with open("./data/equipment.json") as equipment_file:
            data = json.load(equipment_file)
            equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
            try:
                equipment_data = equipment_schema().load(data)
            except marshmallow.exceptions.ValidationError:
                raise ValueError
            # заполнение словарей
            for weapon in equipment_data.weapons:
                self.weapons[weapon.name] = weapon

            for armor in equipment_data.armors:
                self.armors[armor.name] = Armor(id=armor.id, name=armor.name, defence=armor.defence, stamina_per_turn=armor.stamina_per_turn)