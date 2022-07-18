from .event import Event, EventType
from .event_motor import EventMotor
from .memory import Memory
from .reg_file import RegFile
import numpy as np

class InstructionSimulator(EventMotor):
    def __init__(self):
        super().__init__()

        self._memory = Memory()
        self._reg_file = RegFile()
        self._reg_file.reset()
        self._program_counter = 0
        self._instruction = '00000000000000000000000000000000'

        self._events_reactions[EventType.VM_START] = self._start_reaction
        self._events_reactions[EventType.FETCH_DECODE_EXECUTE_STEP] = self._fetch_decode_execute_step_reaction
        self._events_reactions[EventType.FETCH_DECODE_EXECUTE_CONTINUOSLY] = self._fetch_decode_execute_continuosly_reaction
        self._events_reactions[EventType.VM_FINISH] = self._finish_reaction


    def _start_reaction(self, event: Event):
        print("start execution")
        self._reg_file.reset()
        self._program_counter = event.get_data()

    def _fetch_decode_execute_step_reaction(self, event: Event):
        self.fetch_decode_execute()


    def _fetch_decode_execute_continuosly_reaction(self, event: Event):
        self.fetch_decode_execute()
        is_to_stop = self._instruction[0:11] == '11111111111' # stop condition
        if is_to_stop:
            self.add_event(Event(EventType.VM_FINISH, ""))
        else:
            self.add_event(Event(EventType.FETCH_DECODE_EXECUTE_CONTINUOSLY, ""))
    
    def _finish_reaction(self, event: Event):
        print("end execution")
        self.reset()


    def fetch_decode_execute(self):
        self._instruction = f'{self._memory.__getitem__(self._program_counter):032b}'
        self._program_counter += 1 
        print(self._instruction)
        print(self._program_counter)
        print(self._instruction[0:11])


        if self._instruction[0:11] == "11111000010": # LDUR
            print("load started")
            address = int(self._instruction[11:20], base=2)
            print("address :", self._instruction[11:20] )
            rn_value = self._reg_file.__getitem__(int(self._instruction[21:27], base=2))
            rt_address = int(self._instruction[27:32], base = 2)
            rt_value = self._memory.__getitem__(rn_value+address)
            self._reg_file.__setitem__(rt_address, rt_value)   

        elif self._instruction[0:11] == '11111000000': #STUR
            print("store started")
            address = int(self._instruction[11:20], base=2)
            rn_value = self._reg_file.__getitem__(int(self._instruction[21:27], base=2))
            rt_address = int(self._instruction[27:32], base = 2)
            rt_value = self._reg_file.__getitem__(rt_address)
            self._memory.__setitem__(address+rn_value, rt_value)
        
        elif self._instruction[0:8] == '10110100': #CBZ 
            address = int(self._instruction[8:27], base = 2)
            rt_address = int(self._instruction[27:32], base = 2)
            rt_value = self._reg_file.__getitem__(rt_address)
            if rt_value == 0:
                self._program_counter += address
        
        elif self._instruction[0:6] == '000101': #B
            address = int(self._instruction[6:32], base = 2)
            self._program_counter += address

        elif self._instruction[0:6] == '100101': #BL
            self._reg_file.__setitem__(1,self._program_counter + 1)
            address = int(self._instruction[6:32], base = 2)
            self._program_counter += address
        
        elif self._instruction[0:11] == '10001011000': #ADD
            print("add started")
            rn_value = self._reg_file.__getitem__(int(self._instruction[22:27], base = 2))
            rm_value = self._reg_file.__getitem__(int(self._instruction[11:16], base = 2))
            rd_address = int(self._instruction[27:32], base = 2)
            self._reg_file.__setitem__(rd_address, rn_value + rm_value)


        elif self._instruction[0:11] == '11001011000': #SUB
            rn_value = self._reg_file.__getitem__(int(self._instruction[22:27], base = 2))
            rm_value = self._reg_file.__getitem__(int(self._instruction[11:16], base = 2))
            rd_address = self._instruction[27:32]
            self._reg_file.__setitem__(rd_address, rn_value - rm_value)
        
        elif self._instruction[0:11] == '10001010000': #AND
            rn_value = self._reg_file.__getitem__(int(self._instruction[22:27], base = 2))
            rm_value = self._reg_file.__getitem__(int(self._instruction[11:16], base = 2))
            rd_address = self._instruction[27:32]
            self._reg_file.__setitem__(rd_address, rn_value & rm_value)
        
        elif self._instruction[0:11] == '10101010000': #ORR
            rn_value = self._reg_file.__getitem__(int(self._instruction[22:27], base = 2))
            rm_value = self._reg_file.__getitem__(int(self._instruction[11:16], base = 2))
            rd_address = self._instruction[27:32]
            self._reg_file.__setitem__(rd_address, rn_value | rm_value)



    



    






    

