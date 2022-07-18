import re

from .event import Event, EventType
from .event_motor import EventMotor
from .memory import Memory


class AbsoluteAssembler(EventMotor):
    def __init__(self):
        super().__init__()

        # Regex patterns for assembly
        self.patterns = {
            # Matches start directive
            "start": re.compile("start\s+(\d+)"),
            # Matches label and operation mnemonic
            "label": re.compile("([A-Za-z]+):"),
        }

        # Key: mnemonic
        # Value: code
        self.mnemonic_table = {
            "LDUR": "11111000010",
            "STUR": "11111000000",
            "CBZ": "10110100",
            "B": "000101",
            "BL": "100101",
            "ADD": "10001011000",
            "SUB": "11001011000",
            "AND": "10001010000",
            "ORR": "10101010000",
        }

        # Key: label
        # Value: value
        self.symbol_table = {}

        # Helper for assignment of addresses
        self.location_counter = 0

        self._memory = Memory()
        self._events_reactions[
            EventType.ABSOLUTE_ASSEMBLER_FIRST_PASS
        ] = self._first_pass
        self._events_reactions[
            EventType.ABSOLUTE_ASSEMBLER_SECOND_PASS
        ] = self._second_pass
        self._events_reactions[
            EventType.ABSOLUTE_ASSEMBLER_ASSEMBLE_LINE
        ] = self._assemble_line
        self._events_reactions[EventType.ABSOLUTE_ASSEMBLER_END] = self._end

    def _first_pass(self, event: Event):
        with open(event.get_data(), "r") as file:
            first_line = file.readline().lower().strip()
            # If code starts with START mnemonic
            if self.patterns["start"].match(first_line):
                # Set location counter
                self.location_counter = int(
                    self.patterns["start"].match(first_line).groups()[0]
                )
            else:
                self.location_counter = 0
            for line in file:
                print(line)
                print(self.patterns["label"].match(line))

    def _second_pass(self, event: Event):
        pass

    def _assemble_line(self, event: Event):
        pass

    def _end(self, event: Event):
        pass
