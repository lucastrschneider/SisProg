from enum import Enum

class EventType(Enum):
    INVALID_EVENT = 0
    LOADER_LOAD_DATA = 1
    DUMPER_LOAD_DATA = 2
    DUMPER_DUMP_DATA = 3
    FETCH_DECODE_EXECUTE_STEP = 4
    FETCH_DECODE_EXECUTE_CONTINUOSLY = 5
    FINISH = 6

class Event():
    def __init__(self, event_type: EventType, event_data):
        self._type = event_type
        self._data = event_data
    
    def get_type(self) -> EventType:
        return self._type

    def get_data(self):
        return self._data
