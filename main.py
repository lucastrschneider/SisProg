from prog_sys.event import Event, EventType
from prog_sys.memory import Memory
from prog_sys.loader import Loader
from prog_sys.dumper import Dumper

if __name__ == "__main__":
    memory = Memory()
    loader = Loader()
    dumper = Dumper()

    loader.activate()
    dumper.activate()

    load_event = Event(EventType.LOADER_LOAD_DATA, "home/test1.bin")
    status = loader.add_event(load_event)
    status = loader.run()

    dump_event = \
        Event(  EventType.DUMPER_LOAD_DATA,
                {"file": "home/test2.bin",
                "start_address": 15,
                "size": 12 }
        )
    
    status = dumper.add_event(dump_event)
    status = dumper.run()
    status = dumper.run()
