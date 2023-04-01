from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from unit import BaseUnit


class Skill(ABC):
    # базовый класс для скиллов
    def __init__(self, name: str, stamina: int, damage: int) -> None:
        self.name: str = name
        self.stamina: int = stamina
        self.damage: int = damage

    @abstractmethod
    def skill_effect(self, user: BaseUnit, target: BaseUnit) -> str:
        pass

    def use(self, user: BaseUnit, target: BaseUnit) -> str:
        # использование скилла
        if user.stamina >= self.stamina:
            user.stamina -= self.stamina
            return self.skill_effect(user, target)
        return f"{user.name} попытался использовать {self.name} но у него не хватило выносливости."


class FuryPunch(Skill):
    # скилл "Пинок"
    def __init__(self) -> None:
        super().__init__("Пинок", 15, 10)

    def skill_effect(self, user: BaseUnit, target: BaseUnit) -> str:
        target.get_damage(self.damage)
        return f"{user.name} использует {self.name} и наносит {self.damage} урона сопернику"


class HardShot(Skill):
    # скилл "Ваншот"
    def __init__(self) -> None:
        super().__init__("Ваншот", 20, 35)

    def skill_effect(self, user: BaseUnit, target: BaseUnit) -> str:
        target.get_damage(self.damage)
        return f"{user.name} использует {self.name} и наносит {self.damage} урона сопернику"
