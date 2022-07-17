from prog_sys.event import Event, EventType
from prog_sys.memory import Memory
from prog_sys.loader import Loader

if __name__ == "__main__":
    memory = Memory()
    loader = Loader()

    event = Event(EventType.LOAD_DATA_TO_MEMORY, "home/test1.bin")

    loader.activate()
    
    status = loader.add_event(event)
    print(f'Event added {status}')

    status = loader.run()
    print(f'Motor run {status}')

    memory.display()