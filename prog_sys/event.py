from enum import Enum

class EventType(Enum):
    INVALID_EVENT = 0
    LOAD_DATA_TO_MEMORY = 1

class Event():
    def __init__(self, event_type: EventType, event_data):
        self._type = event_type
        self._data = event_data
    
    def get_type(self) -> EventType:
        return self._type

    def get_data(self):
        return self._data
