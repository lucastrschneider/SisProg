from .event import Event, EventType
from .event_motor import EventMotor
from .memory import Memory
from .reg_file import RegFile
from .indicator import Indicator
from enum import Enum
import numpy as np

class VMState(Enum):
    STOPPED = 0
    READY = 1
    RUNNING = 2
    STEPPING = 3

class InstructionSimulator(EventMotor):
    def __init__(self):
        super().__init__()

        self._memory = Memory()
        self._reg_file = RegFile()
        self._reg_file.reset()
        self._program_counter = 0
        self._instruction = '00000000000000000000000000000000'
        self._state = VMState.STOPPED
        Indicator().set_indicator_string("Parada")

        self._events_reactions[EventType.VM_START] = self._start_reaction
        self._events_reactions[EventType.FETCH_DECODE_EXECUTE_STEP] = self._fetch_decode_execute_step_reaction
        self._events_reactions[EventType.FETCH_DECODE_EXECUTE_CONTINUOSLY] = self._fetch_decode_execute_continuosly_reaction
        self._events_reactions[EventType.VM_FINISH] = self._finish_reaction


    def _start_reaction(self, event: Event):
        print("start execution")
        self._reg_file.reset()
        self._program_counter = event.get_data()
        self._state = VMState.READY
        Indicator().set_indicator_string("Preparada")
        Indicator().set_pc(self._program_counter)

    def _fetch_decode_execute_step_reaction(self, event: Event):
        if not self._state == VMState.STOPPED:
            self._state = VMState.STEPPING
            Indicator().set_indicator_string("Passos")
            
            self.fetch_decode_execute()
            Indicator().set_pc(self._program_counter)

            is_to_stop = self._instruction[0:11] == '11111111111' # stop condition
            if is_to_stop:
                self.add_event(Event(EventType.VM_FINISH, ""))

    def _fetch_decode_execute_continuosly_reaction(self, event: Event):
        if not self._state == VMState.STOPPED:
            self._state = VMState.RUNNING
            Indicator().set_indicator_string("Executando")

            self.fetch_decode_execute()
            Indicator().set_pc(self._program_counter)

            is_to_stop = self._instruction[0:11] == '11111111111' # stop condition
            if is_to_stop:
                self.add_event(Event(EventType.VM_FINISH, ""))
            else:
                self.add_event(Event(EventType.FETCH_DECODE_EXECUTE_CONTINUOSLY, ""))
    
    def _finish_reaction(self, event: Event):
        print("end execution")
        self._state = VMState.STOPPED
        Indicator().set_indicator_string("Parada")
        self.reset()


    def fetch_decode_execute(self):
        self._instruction = f'{self._memory[self._program_counter]:032b}'
        self._program_counter += 1 

        if self._instruction[0:11] == "11111000010": # LDUR
            print("load started")
            address = int(self._instruction[11:20], base=2)
            rn_value = self._reg_file[int(self._instruction[21:27], base=2)]
            rt_address = int(self._instruction[27:32], base = 2)
            rt_value = self._memory[rn_value+address]
            self._reg_file[rt_address] = rt_value  

        elif self._instruction[0:11] == '11111000000': #STUR
            print("store started")
            address = int(self._instruction[11:20], base=2)
            rn_value = self._reg_file[int(self._instruction[21:27], base=2)]
            rt_address = int(self._instruction[27:32], base = 2)
            rt_value = self._reg_file[rt_address]
            self._memory[address+rn_value] = rt_value
        
        elif self._instruction[0:8] == '10110100': #CBZ 
            print("compare and branch started")
            address = int(self._instruction[8:27], base = 2) - self._program_counter
            rt_address = int(self._instruction[27:32], base = 2)
            rt_value = self._reg_file[rt_address]
            if rt_value == 0:
                self._program_counter += address
        
        elif self._instruction[0:6] == '000101': #B
            print("branch started")
            address = int(self._instruction[6:32], base = 2) - self._program_counter
            self._program_counter += address


        elif self._instruction[0:6] == '100101': #BL
            print("Branch and Link Started")
            self._reg_file[1] = self._program_counter + 1
            address = int(self._instruction[6:32], base = 2) - self._program_counter
            self._program_counter += address
        
        elif self._instruction[0:11] == '10001011000': #ADD
            print("Add started")
            rn_value = self._reg_file[int(self._instruction[22:27], base = 2)]
            rm_value = self._reg_file[int(self._instruction[11:16], base = 2)]
            rd_address = int(self._instruction[27:32], base = 2)
            self._reg_file[rd_address] = rn_value + rm_value


        elif self._instruction[0:11] == '11001011000': #SUB
            print("Sub started")
            rn_value = self._reg_file[int(self._instruction[22:27], base = 2)]
            rm_value = self._reg_file[int(self._instruction[11:16], base = 2)]
            rd_address = int(self._instruction[27:32], base = 2)
            self._reg_file[rd_address] = rn_value - rm_value
        
        elif self._instruction[0:11] == '10001010000': #AND
            print("And started")
            rn_value = self._reg_file[int(self._instruction[22:27], base = 2)]
            rm_value = self._reg_file[int(self._instruction[11:16], base = 2)]
            rd_address = int(self._instruction[27:32], base = 2)
            self._reg_file[rd_address] = rn_value & rm_value
        
        elif self._instruction[0:11] == '10101010000': #ORR
            print("ORR started")
            rn_value = self._reg_file[int(self._instruction[22:27], base = 2)]
            rm_value = self._reg_file[int(self._instruction[11:16], base = 2)]
            rd_address = int(self._instruction[27:32], base = 2)
            self._reg_file[rd_address] = rn_value | rm_value



    



    






    

