from .singleton import Singleton
import numpy as np

MEMORY_SIZE = 2**10

class Memory(metaclass=Singleton):
    def __init__(self) -> None:
        self.array = np.zeros(MEMORY_SIZE, dtype=np.uint8)


    def __getitem__(self, index):
        return self.array[index]


    def __setitem__(self, index, value):
        self.array[index] = value


    def reset(self):
        self.array *= 0


    def display(self):
        np.savetxt("image.txt", self.array, fmt='%02X')

