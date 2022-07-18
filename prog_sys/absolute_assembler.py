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
            # Matches operation mnemonic
            "opcode": re.compile("([A-Za-z]+)"),
            # Matches end of program
            "end": re.compile("end"),
            # Matches d type instruction operands
            "d_operands": re.compile(r"\[([a-zA-Z0-9]+)\s+\++\s+([a-zA-Z0-9]+)\]"),
        }

        # Key: mnemonic
        # Value: code
        self.mnemonic_table = {
            "ldur": "11111000010",
            "stur": "11111000000",
            "cbz": "10110100",
            "b": "000101",
            "bl": "100101",
            "add": "10001011000",
            "sub": "11001011000",
            "and": "10001010000",
            "orr": "10101010000",
        }

        # Key: label
        # Value: value
        self.symbol_table = {}

        # Key: mnemonic
        # Value: type
        self.type_table = {
            "ldur": "d",
            "stur": "d",
            "cbz": "cb",
            "b": "b",
            "bl": "b",
            "add": "r",
            "sub": "r",
            "and": "r",
            "orr": "r",
        }

        self.register_table = {
            "x0": "00000",
            "x1": "00001",
            "x2": "00010",
            "x3": "00011",
            "x4": "00100",
            "x5": "00101",
            "x6": "00110",
            "x7": "00111",
            "x8": "01000",
            "x9": "01001",
            "x10": "01010",
            "x11": "01011",
            "x12": "01100",
            "x13": "01101",
            "x14": "01110",
            "x15": "01111",
            "x16": "10000",
            "x17": "10001",
            "x18": "10010",
            "x19": "10011",
            "x20": "10100",
            "x21": "10101",
            "x22": "10110",
            "x23": "10111",
            "x24": "11000",
            "x25": "11001",
            "x26": "11010",
            "x27": "11011",
            "x28": "11100",
            "x29": "11101",
            "x30": "11110",
            "x31": "11111",
        }

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
                line = line.lower().strip()
                # Look for end word
                if self.patterns["end"].match(line):
                    break
                # Look for label in line
                if self.patterns["label"].match(line):
                    # Extract label
                    label = self._extract_label(line)
                    # Insert label into symbol table
                    self.symbol_table[label] = self.location_counter
                    # Remove label from line
                    line = line.split(":")[1].strip()

                mnemonic = self._extract_mnemonic(line)
                if mnemonic in self.mnemonic_table:
                    self.location_counter += 4
                elif mnemonic == "word":
                    self.location_counter += 4
                else:
                    print(f"error: mnemonic {mnemonic} not found in mnemonic table")
            print("Symbol table after first pass:")
            print(self.symbol_table)

    def _second_pass(self, event: Event):
        print("second pass")

    def _assemble_line(self, event: Event):
        line = event.get_data().lower().strip()
        object_code = self._assemble_line_handler(line)
        print(object_code, line)
        return object_code

    def _end(self, event: Event):
        print("end")

    def _assemble_line_handler(self, line: str):
        mnemonic = self._extract_mnemonic(line)
        operands = self._extract_operands(line)
        opcode = self.mnemonic_table[mnemonic]

        instruction_type = self.type_table[mnemonic]
        if instruction_type == "d":
            rt = operands[0]
            rn = self.patterns["d_operands"].search(line).groups()[0]
            address = self.patterns["d_operands"].search(line).groups()[1]
            address_justified = self._justify_address(address, 9)
            rt_bin = self.register_table[rt]
            rn_bin = self.register_table[rn]
            object_code = f"{opcode}{address_justified}00{rn_bin}{rt_bin}"
            return object_code
        elif instruction_type == "cb":
            rt = self.register_table[operands[0]]
            address = self._justify_address(operands[1], 19)
            object_code = f"{opcode}{address}{rt}"
            return object_code
        elif instruction_type == "b":
            address = self._justify_address(operands[0], 26)
            object_code = f"{opcode}{address}"
            return object_code
        elif instruction_type == "r":
            rd = self.register_table[operands[0]]
            rn = self.register_table[operands[1]]
            rm = self.register_table[operands[2]]
            shamt = "000000"
            object_code = f"{opcode}{rm}{shamt}{rn}{rd}"
            return object_code
        else:
            return

    def _extract_mnemonic(self, line: str):
        return line.split()[0]

    def _extract_operands(self, line: str):
        # Remove mnemonic from line
        line_operands = line.strip(self._extract_mnemonic(line))
        # Separate operands into list
        operands = [operand.strip() for operand in line_operands.strip().split(",")]

        return operands

    def _extract_label(self, line: str):
        return self.patterns["label"].match(line).groups()[0]

    def _justify_address(self, address: str, target_len):
        # Check if address is absolute
        if address.isnumeric():
            # Convert address from decimal to binary and get string
            bin_address = str(bin(int(address))).strip("0b")
        # If address is relative (label)
        else:
            if address in self.symbol_table:
                bin_address = str(bin(int(self.symbol_table[address]))).strip("0b")
            else:
                bin_address = "?" * target_len

        # Add zeros to the left
        justified_address = "0" * (target_len - len(bin_address)) + bin_address
        return justified_address
