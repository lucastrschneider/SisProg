from .event import Event, EventType
from .event_motor import EventMotor
from .memory import Memory
from .reg_file import RegFile
import numpy as np

class InstructionSimulator(EventMotor):
    def __init__(self,  program_index):
        super().__init__()

        self._memory = Memory()
        self._reg_file = RegFile()
        self._reg_file.reset()
        self._program_counter =  program_index
        self._instruction = '00000000000000000000000000000000'
        self._events_reactions[EventType.FETCH_DECODE_EXECUTE_STEP] = self._first_fetch_decode_execute_step_reaction
        self._events_reactions[EventType.FETCH_DECODE_EXECUTE_CONTINUOSLY] = self._first_fetch_decode_execute_continuosly_reaction
        self._events_reactions[EventType.FINISH] = self._finish_reaction


    def _first_fetch_decode_execute_reaction_step(self):
        self.fetch_decode_execute()


    def _first_fetch_decode_execute_reaction_continuosly(self):
        self.fetch_decode_execute()
        is_to_stop = self._instruction == '11111111111111111111111111111111'
        if is_to_stop:
            self.add_event(Event(EventType.FINISH))
        else:
            self.add_event(Event(EventType.FETCH_DECODE_EXECUTE_CONTINUOSLY))
    
    def _finish_reaction(self):
        self.reset()


    def fetch_decode_execute(self):
        self._instruction = f'{self._memory.__getitem__(self._program_counter):032b}'
        self._program_counter += 1 


        if self._instruction[31:21] == '11111000010': # LDUR
            address = int(self._instruction[20:12], base=2)
            rn_value = self._reg_file.__getitem__(int(self._instruction[9:5], base=2))
            rt_address = int(self._instruction[4:0], base = 2)
            rt_value = self._memory.__getitem__(rn_value+address)
            self._reg_file.__setitem__(rt_address, rt_value)   

        elif self._instruction[31:21] == '11111000000': #STUR
            address = int(self._instruction[20:12], base=2)
            rn_value = self._reg_file.__getitem__(int(self._instruction[9:5], base=2))
            rt_address = int(self._instruction[4:0], base = 2)
            rt_value = self._reg_file.__getitem__(rt_address)
            self._memmory.__setitem__(address+rn_value, rt_value)
        
        elif self._instruction[31:24] == '10110100': #CBZ 
            address = int(self._instruction[23:5], base = 2)
            rt_address = int(self._instruction[4:0], base = 2)
            rt_value = self._reg_file.__getitem__(rt_address)
            if rt_value == 0:
                self._program_counter += address
        
        elif self._instruction[31:26] == '000101': #B
            address = int(self._instruction[25:0], base = 2)
            self._program_counter += address

        elif self._instruction[31:26] == '100101': #BL
            self._reg_file.__setitem__(1,self._program_counter + 1)
            address = int(self._instruction[25:0], base = 2)
            self._program_counter += address
        
        elif self._instruction[31:21] == '10001011000': #ADD
            rn_value = self._reg_file.__getitem__(int(self._instruction[9:5], base = 2))
            rm_value = self._reg_file.__getitem__(int(self._instruction[20:16], base = 2))
            rd_address = self._instruction[4:0]
            self._reg_file.__setitem__(rd_address, rn_value + rm_value)


        elif self._instruction[31:21] == '11001011000': #SUB
            rn_value = self._reg_file.__getitem__(int(self._instruction[9:5], base = 2))
            rm_value = self._reg_file.__getitem__(int(self._instruction[20:16], base = 2))
            rd_address = self._instruction[4:0]
            self._reg_file.__setitem__(rd_address, rn_value - rm_value)
        
        elif self._instruction[31:21] == '10001010000': #AND
            rn_value = self._reg_file.__getitem__(int(self._instruction[9:5], base = 2))
            rm_value = self._reg_file.__getitem__(int(self._instruction[20:16], base = 2))
            rd_address = self._instruction[4:0]
            self._reg_file.__setitem__(rd_address, rn_value & rm_value)
        
        elif self._instruction[31:21] == '10101010000': #ORR
            rn_value = self._reg_file.__getitem__(int(self._instruction[9:5], base = 2))
            rm_value = self._reg_file.__getitem__(int(self._instruction[20:16], base = 2))
            rd_address = self._instruction[4:0]
            self._reg_file.__setitem__(rd_address, rn_value | rm_value)



    



    






    

