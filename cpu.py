"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        

        self.ram = [0] * 256
        self.register = [0] * 8
        self.register[7] = 0xF4
        self.SP = self.register[7]
        self.PC = 0
        self.FL = 0

        # register[5] = IM   <------- Maaaaaaybe?
        # register[6] = IS
        # register[7] = SP
        


    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = []

        

        # if sys.argv[1] is None:
        #     print("This file is bad.")  # for stretch
        #     sys.exit(1)
        try:
            print("try try try trying")
            with open(sys.argv[1]) as f:
                print("Inside the file")
                for line in f:
                    # Process comments:
                    # Ignore anything after a # symbol
                    comment_split = line.split("#")
                    # Convert any numbers from binary strings to integers
                    num = comment_split[0]
                    try:
                        x = int(num, 2)
                    except ValueError:
                        continue
                    # print in binary and decimal
                    print(f"{x:08b}: {x:d}")
                    program.append(x)
        except ValueError:
            print(f"File not found")

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        elif op == "SUB":
            self.register[reg_a] -= self.register[reg_b]
        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]
        elif op == "DIV":
            self.register[reg_a] /= self.register[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        HLT  = 0b00000001
        RET  = 0b00010001
        PUSH = 0b01000101
        POP  = 0b01000110
        PRN  = 0b01000111
        CALL = 0b01010000
        LDI  = 0b10000010
        ADD  = 0b10100000
        SUB  = 0b10100001
        MUL  = 0b10100010
        DIV  = 0b10100011
        MOD  = 0b10100100 #<-------- No clue how to do this yet.  I'll have to look it up.


        running = True

        while running:
            IR = self.ram[self.PC]
            operandA = self.ram_read(self.PC + 1)
            operandB = self.ram_read(self.PC + 2)
            
            if IR == LDI:
                self.register[operandA] = operandB
                self.PC += 3

            elif IR == PRN:
                print(self.register[operandA])
                self.PC += 2

            elif IR == MUL:
                self.alu("MUL", operandA, operandB)
                self.PC += 3

            elif IR == DIV:
                self.alu("DIV", operandA, operandB)
                self.PC += 3

            elif IR == ADD:
                self.alu("ADD", operandA, operandB)
                self.PC += 3

            elif IR == SUB:
                self.alu("SUB", operandA, operandB)
                self.PC += 3

            elif IR == PUSH:
                self.SP -= 1
                self.ram[self.SP] = self.register[operandA]
                self.PC += 2

            elif IR == POP:
                self.register[operandA] = self.ram[self.SP]
                self.SP += 1
                self.PC += 2

            elif IR == HLT:
                running = False
                self.PC += 1

            elif IR == CALL:
                self.SP -= 1
                self.ram[self.SP] = self.PC + 2
                self.PC = self.register[operandA]
                

            elif IR == RET:
                self.PC = self.ram[self.SP]
                self.SP += 1

            else:
                print(f"Unknown Instruction {IR}")
                sys.exit(1)