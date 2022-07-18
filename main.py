from prog_sys.event_controller import EventController
from prog_sys.absolute_assembler import AbsoluteAssembler
from prog_sys.event import Event, EventType
from prog_sys.memory import Memory
from prog_sys.loader import Loader
from prog_sys.dumper import Dumper
from prog_sys.gui import ProgSysGUI

if __name__ == "__main__":
    event_controller = EventController()

    event_controller.register_motor(Loader())
    event_controller.register_motor(Dumper())
    memory = Memory()
    loader = Loader()
    dumper = Dumper()
    absolute_assembler = AbsoluteAssembler()

    loader.activate()
    dumper.activate()
    absolute_assembler.activate()

    gui = ProgSysGUI()

    try:
        gui.start()
    except KeyboardInterrupt:
        gui.stop()
    dump_event = Event(
        EventType.DUMPER_LOAD_DATA,
        {"file": "home/test2.bin", "start_address": 15, "size": 12},
    )

    dump_event = Event(
        EventType.DUMPER_LOAD_DATA,
        {"file": "home/test2.bin", "start_address": 15, "size": 12},
    )

    status = dumper.add_event(dump_event)
    status = dumper.run()
    status = dumper.run()

    assemble_event = Event(EventType.ABSOLUTE_ASSEMBLER_FIRST_PASS, "home/test.asm")
    status = absolute_assembler.add_event(assemble_event)
    status = absolute_assembler.run()
