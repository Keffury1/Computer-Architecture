
import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001

class CPU:

    def __init__(self):
        self.ram = [0] * 256
        self.registers = [0] * 8
        self.pc = 0
        

    def ram_read(self, address):
        return self.ram[address]
    
    def ram_write(self, value, address):
        self.ram[address] = value
    

    def load(self):

        address = 0

        program = [
            0b10000010,
            0b00000000,
            0b00001000,
            0b01000111,
            0b00000000,
            0b00000001,
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
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

        while self.running:
            instruction = self.ram_read(self.pc)

            a = self.ram_read(self.pc + 1)
            b = self.ram_read(self.pc + 2)

            if instruction == HLT:
                self.running = False
                self.pc +=1
            elif instruction == PRN:
                print(self.registers[a])
                self.pc += 2
            elif instruction == LDI:
                self.registers[a] = b
                self.pc += 3

