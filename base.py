from typing import Dict, Optional
from unit import BaseUnit


class BaseSingleton(type):
    # базовый класс
    _instances: Dict[type, 'BaseSingleton'] = {}

    def __call__(cls, *args, **kwargs) -> 'BaseSingleton':
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    # класс поля боя
    STAMINA_PER_ROUND: int = 1

    def start_game(self, player: BaseUnit, enemy: BaseUnit) -> None:
        # начало игры
        self.player: BaseUnit = player
        self.enemy: BaseUnit = enemy
        self.game_is_running: bool = True

    def next_turn(self) -> Optional[str]:
        # следующий раунд
        result = self._check_players_hp()
        if result:
            return result
        if self.game_is_running:
            for character in [self.player, self.enemy]:
                if character.stamina + self.STAMINA_PER_ROUND > character.unit_class.max_stamina:
                    character.stamina = character.unit_class.max_stamina
                elif character.stamina < character.unit_class.max_stamina:
                    character.stamina += self.STAMINA_PER_ROUND
                character.stamina = round(character.stamina, 1)
                character.hit_points = round(character.hit_points, 1)
            return self.enemy.hit(self.player)

    def _check_players_hp(self) -> Optional[str]:
        # завершение боя
        if self.player.hit_points <= 0 and self.enemy.hit_points <= 0:
            return f'Ничья между {self.player.name} и {self.enemy.name}!'
        elif self.player.hit_points >= 0 >= self.enemy.hit_points:
            return f'{self.player.name} победил {self.enemy.name}'
        elif self.player.hit_points <= 0 <= self.enemy.hit_points:
            return f'{self.player.name} проиграл {self.enemy.name}'
        elif self.player.hit_points and self.enemy.hit_points >= 0:
            return None
        return self._end_game()

    def _end_game(self) -> str:
        # конец игры
        self._instances: Dict[type, 'BaseSingleton'] = {}
        result = f"{self.player.name} выходит из боя."
        self.game_is_running = False
        return result

    def player_hit(self) -> str:
        # атака игрока и следующий ход
        result = self.player.hit(self.enemy)
        turn_result = self.next_turn()
        return f"{result}\n{turn_result}"

    def player_use_skill(self) -> str:
        # использование спец. умения
        self.player.use_skill(self.enemy)
        turn_result = self.next_turn()
        return turn_result
