from .event import Event, EventType
from .event_motor import EventMotor
from .memory import Memory

class AbsoluteAssembler(EventMotor):
    def __init__(self):
        super().__init__()

        self._memory = Memory()
        self._events_reactions[EventType.ABSOLUTE_ASSEMBLER_FIRST_STEP] = self._first_step
        self._events_reactions[EventType.ABSOLUTE_ASSEMBLER_SECOND_STEP] = self._second_step
        self._events_reactions[EventType.ABSOLUTE_ASSEMBLER_ASSEMBLE_LINE] = self._assemble_line
        self._events_reactions[EventType.ABSOLUTE_ASSEMBLER_END] = self._end

    def _first_step(self, event: Event):
        pass

    def _second_step(self, event: Event):
        pass

    def _assemble_line(self, event: Event):
        pass

    def end(self, event: Event):
        pass
