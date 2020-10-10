
import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
PUSH = 0b01000101 
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

class CPU:

    def __init__(self):
        self.ram = [0] * 256
        self.registers = [0] * 8
        self.pc = 0
        self.sp = 7
        self.flag = 0B00000000
        

    def ram_read(self, address):
        return self.ram[address]
    
    def ram_write(self, value, address):
        self.ram[address] = value
    

    def load(self):

        if (len(sys.argv)) != 2:
            print("Pass in second file name")
            sys.exit()
 
        try:
            address = 0
            with open(sys.argv[1]) as file:
                for line in file:
                    split = line.split('#')
                    value = split[0].strip()

                    if value == "":
                        continue
                    
                    try:
                        instruction = int(value, 2)
                    except ValueError:
                        print("Invalid Number")
                        sys.exit(1)
                    
                    self.ram[address] = instruction
                    address += 1
        except FileNotFoundError:
            print(f'{sys.argv[1]} file not found')
            sys.exit()



    def alu(self, op, reg_a, reg_b):

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        elif op == "CMP":
            if self.registers[reg_a] < self.registers[reg_b]:
                self.flag = 0b00000100
            if self.registers[reg_a] > self.registers[reg_b]:
                self.flag = 0b00000010
            if self.registers[reg_a] == self.registers[reg_b]:
                self.flag = 0b00000001
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

        self.registers[self.sp] = len(self.ram)

        while self.running:
            instruction = self.ram[self.pc]

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
            elif instruction == MUL:
                self.reg[a] = self.reg[a] * self.reg[b]
                self.pc += 3
            elif instruction == PUSH:
                register = self.ram[self.pc + 1]
                value = self.registers[register]
                self.registers[self.sp] -= 1
                self.ram[self.registers[self.sp]] = value
                self.pc += 2
            elif instruction == POP:
                register = self.ram[self.pc + 1]
                value = self.ram[self.registers[self.sp]]
                self.registers[register] = value
                self.registers[self.sp] += 1
                self.pc += 2
            elif instruction == CALL:
                return_address = self.pc + 2
                self.registers[self.sp] -= 1
                self.ram[self.registers[self.sp]] = return_address

                register = self.ram[self.pc + 1]
                subroutine_address = self.registers[register]
                self.pc = subroutine_address
            elif instruction == RET:
                return_address = self.registers[self.sp]
                self.pc = self.ram[return_address]
                self.registers[self.sp] += 1
            elif instruction == CMP:
                self.alu("CMP", a, b)
                self.pc += 3
            elif instruction == JMP:
                self.pc = self.registers[a]
            elif instruction == JEQ:
                if self.flag == 0b00000001:
                    self.pc = self.registers[a]
                else:
                    self.pc += 2
            elif instruction == JNE:
                if self.flag != 0b00000001:
                    self.pc = self.registers[a]
                else:
                    self.pc += 2
            else:
                self.pc += 1