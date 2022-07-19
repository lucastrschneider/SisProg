from enum import Enum


class EventType(Enum):
    INVALID_EVENT = 0
    LOADER_LOAD_DATA = 1
    DUMPER_LOAD_DATA = 2
    DUMPER_DUMP_DATA = 3
    VM_START = 4
    FETCH_DECODE_EXECUTE_STEP = 5
    FETCH_DECODE_EXECUTE_CONTINUOSLY = 6
    VM_FINISH = 7
    ABSOLUTE_ASSEMBLER_FIRST_PASS = 8
    ABSOLUTE_ASSEMBLER_SECOND_PASS = 9
    ABSOLUTE_ASSEMBLER_ASSEMBLE_LINE = 10
    ABSOLUTE_ASSEMBLER_END = 11


class Event():
    def __init__(self, event_type: EventType, event_data):
        self._type = event_type
        self._data = event_data

    def get_type(self) -> EventType:
        return self._type

    def get_data(self):
        return self._data
