
import sys

class CPU:

    def __init__(self):
        self.ram = [0] * 256
        self.registers = [0] * 8
        self.pc = 0
        self.sp = 7
        self.ir = 0
        self.Flags = [0]*8
        

    def ram_read(self, address):
        return self.ram[address]
    
    def ram_write(self, value, address):
        self.ram[address] = value
    

    def load(self):

        address = 0
        
        print(sys.argv)

        if len(sys.argv) != 2:
            print(f'USAGE')
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    split = line.split('#')
                    value = split[0].strip()

                    if value == '':
                        continue
                        
                    instruction = int(value, 2)
                    self.ram[address] = instruction
                    address += 1
        except FileNotFoundError:
            print(f'file not found')
            sys.exit(2)


    def alu(self, op, reg_a, reg_b):

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            sum = self.reg[reg_a] * self.reg[reg_b]
            self.reg[reg_a] = sum
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        self.running = True

        self.registers[self.sp] = len(self.ram) - 1

        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        POP = 0b01000110
        PUSH = 0b01000101
        CALL = 0b01010000
        RET = 0b00010001
        CMP = 0b10100111
        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110
        GREATER_THAN = 0
        LESS_THAN = 0
        EQUAL = 0

        while self.running:
            instruction = self.ram[self.pc]

            a = self.ram_read(self.pc + 1)
            b = self.ram_read(self.pc + 2)

            if instruction == HLT:
                self.running = False
            elif instruction == PRN:
                print(self.registers[a])
                self.pc += 2
            elif instruction == LDI:
                self.registers[a] = b
                self.pc += 3
            elif instruction == MUL:
                c = self.ram_read(self.pc + 1)
                d = self.ram_read(self.pc + 2)
                self.alu('MUL', c, d)
                self.pc += 3
            elif instruction == PUSH:
                reg = self.ram_read(self.pc + 1)
                reg_val = self.reg[reg]
                self.reg[self.sp] -= 1
                self.ram[self.reg[self.sp]] = reg_val
                self.pc += 2
            elif instruction == POP:
                value = self.ram[self.reg[self.sp]]
                reg = self.ram_read(self.pc + 1)
                self.reg[reg] = value
                self.reg[self.sp] += 1
                self.pc += 2
            elif instruction == CALL:
                val = self.pc+2
                reg = self.ram[self.pc+1]
                sub_address = self.reg[reg]
                self.reg[self.sp] -= 1
                self.ram[self.reg[self.sp]] = val
                self.pc = sub_address
            elif instruction == RET:
                return_add = self.reg[self.sp]
                self.pc = self.ram[return_add]
                self.reg[self.sp] += 1
            elif instruction == CMP:
                self.Flags = CMP
                if self.reg[self.ram_read(self.pc+1)] < self.reg[self.ram_read(self.pc+2)]:
                    GREATER_THAN = 0
                    LESS_THAN = 1
                    EQUAL = 0
                    self.Flags = 0b00000100
                elif self.reg[self.ram_read(self.pc+1)] > self.reg[self.ram_read(self.pc+2)]:
                    GREATER_THAN = 1
                    LESS_THAN = 0
                    EQUAL = 0
                    self.Flags = 0b00000010
                elif self.reg[self.ram_read(self.pc+1)] == self.reg[self.ram_read(self.pc+2)]:
                    GREATER_THAN = 0
                    LESS_THAN = 0
                    EQUAL = 1
                    self.Flags = 0b00000001
                self.pc += 3
            elif instruction == JEQ:
                if EQUAL == 1:
                    self.pc = self.reg[self.ram_read(self.pc+1)]
                else:
                    self.pc += 2
            elif instruction == JNE:
                if EQUAL == 0:
                    self.pc = self.reg[self.ram_read(self.pc+1)]
                else:
                    self.pc += 2
            elif instruction == JMP:
                self.pc = self.reg[self.ram_read(self.pc+1)]

