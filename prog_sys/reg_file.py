from .singleton import Singleton
import numpy as np

MEMORY_SIZE = 2**5

class RegFile(metaclass=Singleton):
    def __init__(self) -> None:
        self.array = np.zeros(MEMORY_SIZE, dtype=np.uint32)

    def __getitem__(self, index) -> np.uint32:
        return self.array[index]

    def __setitem__(self, index, value: np.uint32):
        self.array[index] = value

    def reset(self):
        self.array *= 0

    def display(self):
        np.savetxt("reg_display.txt", self.array, fmt='%08X')