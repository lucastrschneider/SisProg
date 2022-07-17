from .event import Event, EventType
from .event_motor import EventMotor
from .memory import Memory

class Loader(EventMotor):
    def __init__(self):
        super().__init__()

        self._memory = Memory()
        self._events_reactions[EventType.LOADER_LOAD_DATA] = self._load_data_reaction

    def _load_data_reaction(self, event: Event):
        with open(event.get_data(), 'r') as file:
            address = int(file.readline(), base=16)
            for line in file:
                data = int(line, base=16)
                self._memory[address] = data
                address = address + 1