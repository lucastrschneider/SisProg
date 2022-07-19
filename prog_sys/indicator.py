from .singleton import Singleton

class Indicator(metaclass=Singleton):
    def __init__(self) -> None:
        self._indicator_string = None
        self._pc = 0

    def set_indicator_string(self, indicator_str: str):
        self._indicator_string = indicator_str

    def get_indicator_string(self):
        return self._indicator_string

    def set_pc(self, pc: int):
        self._pc = pc

    def get_pc(self):
        return self._pc