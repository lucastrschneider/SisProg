from .event import Event, EventType
from queue import Queue

class EventMotor():
    def __init__(self):
        self._events_queue = Queue();

        self._events_reactions = {
            EventType.INVALID_EVENT : None
        }

        self._active = True

    def activate(self):
        self._active = True
    
    def deactivate(self):
        self._active = False

    def add_event(self, event:Event) -> bool:
        if event.get_type() in self._events_reactions.keys():
            self._events_queue.put(event, block=False);
            return True

        return False

    def run(self) -> bool:
        if self._active:
            if not self._events_queue.empty():
                event = self._events_queue.get(block=False)
                reaction = self._events_reactions[event.get_type()]
                if callable(reaction):
                    reaction(event)
                    return True

        return False
