from queue import Queue
from .singleton import Singleton
from .event import Event
from .event_motor import EventMotor

class EventController(metaclass=Singleton):
    def __init__(self) -> None:
        self._events_queue = Queue();
        self._motors_list = []
    
    def register_motor(self, event_motor: EventMotor):
        self._motors_list.append(event_motor)

    def add_event(self, event: Event):
        self._events_queue.put(event, block=False);

    def run(self):
        while not self._events_queue.empty():
            event = self._events_queue.get(block=False)
            for motor in self._motors_list:
                motor.add_event(event)

        for motor in self._motors_list:
            motor.run()