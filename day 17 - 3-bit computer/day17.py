import re
import os
import math
from enum import Enum

class Register(Enum):
    A = 0
    B = 1
    C = 2

class Opcode(Enum):
    adv = 0
    bxl = 1
    bst = 2
    jnz = 3
    bxc = 4
    out = 5
    bdv = 6
    cdv = 7

class ChronospatialComputer:
    def __init__(self, registers: list):
        self.__initialRegisters = registers
        self.reset()
    
    def reset(self):
        self.registers = {
            Register.A: self.__initialRegisters[0],
            Register.B: self.__initialRegisters[1],
            Register.C: self.__initialRegisters[2]
        }

    def getComboOperand(self, operand: int):
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return self.registers[Register.A]
            case 5:
                return self.registers[Register.B]
            case 6:
                return self.registers[Register.C]
            case _:
                return None
            
    def run(self, program: str | list):
        output = []
        pointer = 0

        while pointer < len(program):
            op = Opcode(program[pointer])
            operand = program[pointer+1]
            comboOperand = self.getComboOperand(operand)

            match op:
                case Opcode.adv:
                    result = self.registers[Register.A] // (2**comboOperand)
                    self.registers[Register.A] = result
                    pointer += 2

                case Opcode.bxl:
                    self.registers[Register.B] ^= operand
                    pointer += 2

                case Opcode.bst:
                    self.registers[Register.B] = comboOperand % 8
                    pointer += 2
                
                case Opcode.jnz:
                    if self.registers[Register.A] != 0:
                        pointer = operand
                    else:
                        pointer += 2
                
                case Opcode.bxc:
                    self.registers[Register.B] ^= self.registers[Register.C]
                    pointer += 2
                
                case Opcode.out:
                    output.append(comboOperand % 8)
                    pointer += 2

                case Opcode.bdv:
                    result = self.registers[Register.A] // (2**comboOperand)
                    self.registers[Register.B] = result
                    pointer += 2
                
                case Opcode.cdv:
                    result = self.registers[Register.A] // (2**comboOperand)
                    self.registers[Register.C] = result
                    pointer += 2

                case _:
                    print("Invalid operation. Program halted.")
                    return

        return ','.join(str(i) for i in output)

def main(fileName):
    currentFilePath = os.path.abspath(f'{os.path.dirname(__file__)}/{fileName}.txt')
    with open(currentFilePath, mode="r") as file:
        registerValues, program = file.read().split("\n\n")
    registerValues = [int(i) for i in re.findall(r'[0-9]+', registerValues)]
    program = [int(i) for i in re.findall(r'[0-9]+', program)]
    
    chronocomputer = ChronospatialComputer(registerValues)
    output = chronocomputer.run(program)
    print(output)


main("example")
main("input")
main("example2")