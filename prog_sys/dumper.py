from .event import Event, EventType
from .event_motor import EventMotor
from .memory import Memory
import numpy as np

class Dumper(EventMotor):
    def __init__(self):
        super().__init__()

        self._memory = Memory()
        self._events_reactions[EventType.DUMPER_LOAD_DATA] = self._load_data_reaction
        self._events_reactions[EventType.DUMPER_DUMP_DATA] = self._dump_data_reaction

    def _load_data_reaction(self, event: Event):
        dump_start_address = event.get_data()['start_address']
        dump_size = event.get_data()['size']

        array = np.zeros(dump_size, dtype=np.uint32)
        for i in range(dump_size):
            array[i] = self._memory[dump_start_address + i]

        dump_event_data = {}
        dump_event_data['file'] = event.get_data()['file']
        dump_event_data['start_address'] = event.get_data()['start_address']
        dump_event_data['words'] = array

        dump_event = Event(EventType.DUMPER_DUMP_DATA, dump_event_data)
        self.add_event(dump_event)

    def _dump_data_reaction(self, event: Event):
        header = f"{event.get_data()['start_address']:03x}"
        np.savetxt(event.get_data()['file'], event.get_data()['words'], fmt='%08X', header=header, comments='')