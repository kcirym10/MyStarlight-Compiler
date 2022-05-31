from multiprocessing.sharedctypes import Value
from compiler.helper import structsFromFile
from compiler.virtualMemory import memoryArchitecture

class memory:
    def __init__(self, memType):
        self.memory = [{}, {}, {}]
        self.memType = memoryArchitecture[memType]

    def mapMemory(self, address):
        keyList = list(self.memType.keys())
        #print(keyList)
        for key, value in self.memType.items():
            #print(key," ",keyList.index(key))
            startRange = self.memType[key]
            if int(address) >= startRange and int(address) < startRange + 2000:
                return self.memory[keyList.index(key)]

    def getValue(self, address):
        #print(self.mapMemory(address))
        return self.mapMemory(address)[address]

    def setValue(self, address, val):
        self.mapMemory(address)[address] = val
        

        #print(self.memory)


class virtualMachine:
    constants = None
    quadList = None
    memLimit = 1000

    # Declare memory structure as mem = []
    def __init__(self):
        self._globalMemory = memory("GS")
        self._localMemory = [memory("LS")]
        self._tempMemory = [memory("TS")]
        self._constantMemory = memory("CS")
        self.memUsage = 0

    # The Memory Segment function
    # Returns the appropriate memory to use
    # Based on the range in which an address is located
    def memSeg(self, address):
        if address < 6000:
            return self._globalMemory
        if address < 12000:
            return self._localMemory[-1]
        if address < 18000:
            return self._tempMemory[-1]
        return self._constantMemory

    def populateConstants(self, constants):
        for key, value in constants.items():
            self.memSeg(int(key)).setValue(int(key), value)
            self.memUsage += 1

    # Check user input
    # Checks the type of the value user has inputed through the terminal and
    # returns the appropriate object type (int, float, string)
    def checkUserInput(self, input):
        try:
            return int(input)
        except ValueError:
            try:
                return float(input)
            except ValueError:
                return input

    # Set Read Input (not the most elegant solution -- **May Change**)
    # This function checks the address range stored in a3 and if it is either
    # integer or floating point it checks wether the received user input is actually
    # and instance of the correct type
    def setReadInput(self, temp, a3):
        # Global Segment
        if a3 < 2000:
            if isinstance(temp, int):
                self.memSeg(a3).setValue(a3, temp)
            else:
                print("Type Mismatch in user input")
                return
        elif a3 < 4000:
            if isinstance(temp, float):
                self.memSeg(a3).setValue(a3, temp)
            else:
                print("Type Mismatch in user input")
                return
        elif a3 < 6000:
            self.memSeg(a3).setValue(a3, str(temp)[0])
        # Local Segment
        elif a3 < 8000:
                if isinstance(temp, int):
                    self.memSeg(a3).setValue(a3, temp)
                else:
                    print("Type Mismatch in user input")
                    return
        elif a3 < 10000:
                if isinstance(temp, float):
                    self.memSeg(a3).setValue(a3, temp)
                else:
                    print("Type Mismatch in user input")
                    return
        elif a3 < 12000:
            print("Address ", a3, "\n",a3 % 4000, "\n\n")
            self.memSeg(a3).setValue(a3, str(temp)[0])

    # This function runs all the instructions that are in the
    # quadrple list.
    def runInstructions(self):
        ip = 0
        while (self.quadList[ip][0] != "ENDPROGRAM"):
            #print(self.memUsage)
            quad = self.quadList[ip]
            #print(quad)
            #print(ip)
            quadCode = quad[0]
            # Special
            # GOTO's always require a continue at the end in order to keep the
            # ip from changing after setting it
            if quadCode == "GOTO":
                ip = int(quad[3])
                continue
            elif quadCode == 'GOTOF':
                a1 = int(quad[1])
                if self.memSeg(a1).getValue(a1) == False:
                    ip = int(quad[3])
                    continue
            # Reading and Writting
            elif quadCode == "PRINT":
                a3 = int(quad[3])
                #print(self.memSeg(a1))
                print(self.memSeg(a3).getValue(a3))
            elif quadCode == "READ":
                # must check for the expected type if not raise error
                a3 = int(quad[3])
                temp = input()
                # Validate if input is empty and keep on requesting it
                while temp == "":
                    temp = input()
                
                temp = self.checkUserInput(temp)
                self.setReadInput(temp, a3)
                self.memUsage += 1
            # Expressions
            elif quadCode == "=":
                a1 = int(quad[1])
                a3 = int(quad[3])
                #print(self.memSeg(a1))
                res = self.memSeg(a1).getValue(a1)
                self.memSeg(a3).setValue(a3, res)
                self.memUsage += 1
            elif quadCode == "&":
                a1 = int(quad[1])
                a2 = int(quad[2])
                a3 = int(quad[3])
                res = self.memSeg(a1).getValue(a1) and self.memSeg(a2).getValue(a2)
                self.memSeg(a3).setValue(a3, res)
                self.memUsage += 1
            elif quadCode == "|":
                a1 = int(quad[1])
                a2 = int(quad[2])
                a3 = int(quad[3])
                res = self.memSeg(a1).getValue(a1) or self.memSeg(a2).getValue(a2)
                self.memSeg(a3).setValue(a3, res)
                self.memUsage += 1
            elif quadCode == ">":
                a1 = int(quad[1])
                a2 = int(quad[2])
                a3 = int(quad[3])
                res = self.memSeg(a1).getValue(a1) > self.memSeg(a2).getValue(a2)
                self.memSeg(a3).setValue(a3, res)
                self.memUsage += 1
            elif quadCode == "<":
                a1 = int(quad[1])
                a2 = int(quad[2])
                a3 = int(quad[3])
                res = self.memSeg(a1).getValue(a1) < self.memSeg(a2).getValue(a2)
                self.memSeg(a3).setValue(a3, res)
                self.memUsage += 1
            elif quadCode == ">=":
                a1 = int(quad[1])
                a2 = int(quad[2])
                a3 = int(quad[3])
                res = self.memSeg(a1).getValue(a1) >= self.memSeg(a2).getValue(a2)
                self.memSeg(a3).setValue(a3, res)
                self.memUsage += 1
            elif quadCode == "<=":
                a1 = int(quad[1])
                a2 = int(quad[2])
                a3 = int(quad[3])
                res = self.memSeg(a1).getValue(a1) <= self.memSeg(a2).getValue(a2)
                self.memSeg(a3).setValue(a3, res)
                self.memUsage += 1
            elif quadCode == "==":
                a1 = int(quad[1])
                a2 = int(quad[2])
                a3 = int(quad[3])
                res = self.memSeg(a1).getValue(a1) == self.memSeg(a2).getValue(a2)
                self.memSeg(a3).setValue(a3, res)
                self.memUsage += 1
            elif quadCode == "!=":
                a1 = int(quad[1])
                a2 = int(quad[2])
                a3 = int(quad[3])
                res = self.memSeg(a1).getValue(a1) != self.memSeg(a2).getValue(a2)
                self.memSeg(a3).setValue(a3, res)
                self.memUsage += 1
            elif quadCode == "+":
                a1 = int(quad[1])
                a2 = int(quad[2])
                a3 = int(quad[3])
                res = self.memSeg(a1).getValue(a1) + self.memSeg(a2).getValue(a2)
                self.memSeg(a3).setValue(a3, res)
                self.memUsage += 1
            elif quadCode == "-":
                a1 = int(quad[1])
                a2 = int(quad[2])
                a3 = int(quad[3])
                res = self.memSeg(a1).getValue(a1) - self.memSeg(a2).getValue(a2)
                self.memSeg(a3).setValue(a3, res)
                self.memUsage += 1
            elif quadCode == "*":
                a1 = int(quad[1])
                a2 = int(quad[2])
                a3 = int(quad[3])
                res = self.memSeg(a1).getValue(a1) * self.memSeg(a2).getValue(a2)
                self.memSeg(a3).setValue(a3, res)
                self.memUsage += 1
            elif quadCode == "/":
                a1 = int(quad[1])
                a2 = int(quad[2])
                a3 = int(quad[3])
                val1 = self.memSeg(a1).getValue(a1)
                val2 = self.memSeg(a2).getValue(a2)
                if val2 != 0:
                    res = val1 / val2
                    self.memSeg(a3).setValue(a3, res)
                    self.memUsage += 1
                else:
                    print("ERROR division by 0 not supported")
            ip += 1



    def run(self):
        constants, self.quadList = structsFromFile()
        #printQuad(self.quadList)
        #print(constants)
        self.populateConstants(constants)
        # gm = memory("GS")
        # gm.setValue('3100', 10)
        # print(gm.getValue('3100'))
        self.runInstructions()

def printQuad(quadList):
    columns = 3

    index = 0
    formatted = ''
    for quad in quadList:
        if isinstance(quad[3], list):
            formatted += f'{index})\t{quad[0]}\t{quad[1]}\t{quad[2]}\t{quad[3]}\t'
        else:
            formatted += f'{index})\t{quad[0]}\t{quad[1]}\t{quad[2]}\t{quad[3]}\t\t\t'
        index += 1
        if index % columns == 0:
            formatted += '\n'
    
    print(formatted)