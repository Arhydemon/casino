from abc import ABC, abstractmethod

# эт у мя базовая сущность
# наследуются плеер, гейрезульт, сеттингс, статистика, аппстейт, базгейм
class BaseEntity(ABC):
    @abstractmethod
    def compare_value(self):
        raise NotImplementedError

    @abstractmethod
    def display_text(self) -> str:
        raise NotImplementedError

    # ТУТ УСЛОВИЯ ДЛЯ ЭКЗАМЕНА Я РЕШИЛ ВЫПОЛНИТЬ
    def __str__(self) -> str: # суть "типа красиво" показать объект человеку
        return self.display_text()

    def __repr__(self) -> str: # для отладки, показать объект в консоли
        return f"{self.__class__.__name__}({self.display_text()})"

    def __eq__(self, other) -> bool: # сравнение объекта на равенство
        if not isinstance(other, self.__class__): # isinstance это проверка, что other такого же класса как и self
            return False
        return self.compare_value() == other.compare_value()

    def __lt__(self, other) -> bool: # какой больше какой меньше
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.compare_value() < other.compare_value()

# ПРОВЕРКА CRTL + /
# if __name__ == "__main__":
#     class Player(BaseEntity):
#         def __init__(self, name: str, balance: int) -> None:
#             self.name = name
#             self.balance = balance

#         def compare_value(self):
#             # сравниваю игроков по балансу
#             return self.balance

#         def display_text(self) -> str:
#             # текст для print(player)
#             return f"{self.name}: {self.balance}"

#     player1 = Player("Макар", 500)
#     player2 = Player("Иван", 1000)
#     print(player1)
#     print([player1])
#     print(player1 == player2)
#     print(player1 < player2)