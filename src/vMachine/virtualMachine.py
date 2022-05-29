from compiler.helper import structsFromFile
from compiler.virtualMemory import memoryArchitecture

class memory:
    def __init__(self, memType):
        self.memory = [{}, {}, {}]
        self.memType = memoryArchitecture[memType]

    def mapMemory(self, address):
        keyList = list(self.memType.keys())
        for key, value in self.memType.items():
            print(key," ",keyList.index(key))
            startRange = self.memType[key]
            if int(address) >= startRange and int(address) < startRange + 2000:
                return self.memory[keyList.index(key)]

    def getValue(self, address):
        return self.mapMemory(address)[address]

    def setValue(self, address, val):
        self.mapMemory(address)[address] = val

        print(self.memory)


class virtualMachine:
    constants = None
    quadList = None

    # Declare memory structure as mem = []
    def __init__(self):
        self._globalMemory = memory("GS")
        self._localMemory = [memory("LS")]
        self._tempMemory = [memory("TS")]
        self._constantMemory = memory("CS")

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

    # This function runs all the instructions that are in the
    # quadrple list.
    def runInstructions(self):
        ip = 0
        while (self.quadList[ip][0] != "ENDPROGRAM"):
            quad = self.quadList[ip]
            print(quad)
            print(ip)
            quadCode = quad[0]
            # Special
            if quadCode == "GOTO":
                ip = int(quad[3])
                continue
            
            # Expressions
            elif quadCode == "=":
                a1 = int(quad[1])
                a3 = int(quad[3])
                print(self.memSeg(a1))
                res = self.memSeg(a1).getValue(a1)
                self.memSeg(a3).setValue(a3, res)
            elif quadCode == "&":
                a1 = int(quad[1])
                a2 = int(quad[2])
                a3 = int(quad[3])
                res = self.memSeg(a1).getValue(a1) and self.memSeg(a2).getValue(a2)
                self.memSeg(a3).setValue(a3, res)
            elif quadCode == "|":
                a1 = int(quad[1])
                a2 = int(quad[2])
                a3 = int(quad[3])
                res = self.memSeg(a1).getValue(a1) or self.memSeg(a2).getValue(a2)
                self.memSeg(a3).setValue(a3, res)
            elif quadCode == ">":
                a1 = int(quad[1])
                a2 = int(quad[2])
                a3 = int(quad[3])
                res = self.memSeg(a1).getValue(a1) > self.memSeg(a2).getValue(a2)
                self.memSeg(a3).setValue(a3, res)
            elif quadCode == "<":
                a1 = int(quad[1])
                a2 = int(quad[2])
                a3 = int(quad[3])
                res = self.memSeg(a1).getValue(a1) < self.memSeg(a2).getValue(a2)
                self.memSeg(a3).setValue(a3, res)
            elif quadCode == ">=":
                a1 = int(quad[1])
                a2 = int(quad[2])
                a3 = int(quad[3])
                res = self.memSeg(a1).getValue(a1) >= self.memSeg(a2).getValue(a2)
                self.memSeg(a3).setValue(a3, res)
            elif quadCode == "<=":
                a1 = int(quad[1])
                a2 = int(quad[2])
                a3 = int(quad[3])
                res = self.memSeg(a1).getValue(a1) <= self.memSeg(a2).getValue(a2)
                self.memSeg(a3).setValue(a3, res)
            elif quadCode == "==":
                a1 = int(quad[1])
                a2 = int(quad[2])
                a3 = int(quad[3])
                res = self.memSeg(a1).getValue(a1) == self.memSeg(a2).getValue(a2)
                self.memSeg(a3).setValue(a3, res)
            elif quadCode == "!=":
                a1 = int(quad[1])
                a2 = int(quad[2])
                a3 = int(quad[3])
                res = self.memSeg(a1).getValue(a1) != self.memSeg(a2).getValue(a2)
                self.memSeg(a3).setValue(a3, res)
            elif quadCode == "+":
                a1 = int(quad[1])
                a2 = int(quad[2])
                a3 = int(quad[3])
                res = self.memSeg(a1).getValue(a1) + self.memSeg(a2).getValue(a2)
                self.memSeg(a3).setValue(a3, res)
            elif quadCode == "-":
                a1 = int(quad[1])
                a2 = int(quad[2])
                a3 = int(quad[3])
                res = self.memSeg(a1).getValue(a1) - self.memSeg(a2).getValue(a2)
                self.memSeg(a3).setValue(a3, res)
            elif quadCode == "*":
                a1 = int(quad[1])
                a2 = int(quad[2])
                a3 = int(quad[3])
                res = self.memSeg(a1).getValue(a1) * self.memSeg(a2).getValue(a2)
                self.memSeg(a3).setValue(a3, res)
            elif quadCode == "/":
                a1 = int(quad[1])
                a2 = int(quad[2])
                a3 = int(quad[3])
                val1 = self.memSeg(a1).getValue(a1)
                val2 = self.memSeg(a2).getValue(a2)
                if val2 != 0:
                    res = val1 / val2
                    self.memSeg(a3).setValue(a3, res)
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