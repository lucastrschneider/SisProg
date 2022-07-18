from prog_sys.event import Event, EventType
from prog_sys.memory import Memory
from prog_sys.reg_file import RegFile
from prog_sys.loader import Loader
from prog_sys.dumper import Dumper
from prog_sys.instruction_simulator import InstructionSimulator

if __name__ == "__main__":
    memory = Memory()
    reg_file = RegFile()
    loader = Loader()
    dumper = Dumper()
    vm = InstructionSimulator(48)

    loader.activate()
    dumper.activate()
    vm.activate()

    load_event1 = Event(EventType.LOADER_LOAD_DATA, "home/test1.bin")
    load_event2 = Event(EventType.LOADER_LOAD_DATA, "home/test3.bin")

    vm_event = Event(EventType.FETCH_DECODE_EXECUTE_CONTINUOSLY, "")

    status = loader.add_event(load_event1)
    status = loader.add_event(load_event2)
    status = loader.run()
    status = loader.run()
    status = vm.add_event(vm_event)
    for i in range(6):
        status = vm.run()
    reg_file.display()


    memory.display()

    # dump_event = \
    #     Event(  EventType.DUMPER_LOAD_DATA,
    #             {"file": "home/test2.bin",
    #             "start_address": 15,
    #             "size": 12 }
    #     )
    
    # status = dumper.add_event(dump_event)
    # status = dumper.run()
    # status = dumper.run()