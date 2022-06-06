from multiprocessing.sharedctypes import Value
from re import A
from compiler.helper import structsFromFile
from compiler.virtualMemory import memoryArchitecture

class memory:
    def __init__(self, memType, memSize = 0):
        self.memory = [{}, {}, {}, {}]
        self.memType = memoryArchitecture[memType]
        self.memSize = memSize

    def mapMemory(self, address):
        keyList = list(self.memType.keys())
        #print(keyList)
        for key, value in self.memType.items():
            startRange = self.memType[key]
            if int(address) >= startRange and int(address) < startRange + 2000:
                if int(address) not in self.memory[keyList.index(key)]:
                    if key == 'char':
                        self.memory[keyList.index(key)][int(address)] = str(0)
                    else:
                        self.memory[keyList.index(key)][int(address)] = 0
                return self.memory[keyList.index(key)]

    def getValue(self, address):
        if address >= 18000 and address < 20000:
            pointerAddress = self.mapMemory(address)[address]
            # print('pointer address in getVal ', pointerAddress)
            if gM.mapMemory(pointerAddress) is not None:
                return gM.mapMemory(pointerAddress)[pointerAddress]
            else:
                return lM[-1].mapMemory(pointerAddress)[pointerAddress]
        return self.mapMemory(address)[address]

    def setValue(self, address, val):
        if address >= 18000 and address < 20000:
            pointerAddress = self.mapMemory(address)[address]
            # print("Pointer Address ", pointerAddress)
            if gM.mapMemory(pointerAddress) is not None:
                gM.mapMemory(pointerAddress)[pointerAddress] = val
            else:
                lM[-1].mapMemory(pointerAddress)[pointerAddress] = val
        self.mapMemory(address)[address] = val
        

        #print(self.memory)

gM = memory("GS")
lM = [memory("LS")]
tM = [memory("TS")]
cM = memory("CS")

class virtualMachine:
    constants = None
    quadList = None
    memLimit = 100000

    # Declare memory structure as mem = []
    def __init__(self):
        self._globalMemory = gM
        self._localMemory = lM
        self._tempMemory = tM
        self._constantMemory = cM
        self.memUsage = 0
        self.tempContext = None
        self._jumpStack = []

    # The Memory Segment function
    # Returns the appropriate memory to use
    # Based on the range in which an address is located
    def memSeg(self, address):
        if address < 6000:
            return self._globalMemory
        if address < 12000:
            return self._localMemory[-1]
        if address < 20000:
            return self._tempMemory[-1]
        return self._constantMemory

    def removeContext(self):
        self._localMemory.pop()
        self._tempMemory.pop()

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
        runTimeError = ""
        ip = 0
        while (self.quadList[ip][0] != "ENDPROGRAM"):
            # Check memory usage in case new variables were created and size not modified in recursive call
            if self.memUsage > self.memLimit:
                runTimeError = "Stack Overflow"
            # Check and possibly throw execution error
            if runTimeError != "":
                print(runTimeError)
                return
            #print(self.memUsage)
            quad = self.quadList[ip]
            # print(quad)
            # print(ip)
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
            # Function
            elif quadCode == "ERA":
                itemCount = 0
                index = 0
                segSize = [0,0]
                # Convert the 6 numbers into a list to be processed for the temp and local sizes
                sizeList = list(quad[3].split(" "))
                for item in sizeList:
                        if itemCount == 3:
                            index = 1
                        segSize[index] += int(item)

                if self.memUsage + segSize[0] + segSize[1] > self.memLimit:
                    runTimeError = "Stack Overflow"
                
                # Create a temporarily parallel memory context before changing to it
                self.tempContext = [memory("LS", segSize[0]), memory("TS", segSize[1])]
                # print(quad[3])
                # print(f"ERA size = {segSize[0] + segSize[1]}")
            elif quadCode == "PARAM":
                # The parameter is saved to the local memory because it is not
                # an intermediate calculation
                a1 = int(quad[1])
                a3 = int(quad[3])
                self.tempContext[0].setValue(a3, self.memSeg(a1).getValue(a1))
            elif quadCode == "GOSUB":
                # Change context
                self._localMemory.append(self.tempContext[0])
                self._tempMemory.append(self.tempContext[1])
                # Save current IP and change the IP
                self._jumpStack.append(ip)
                ip = int(quad[3])
                continue
            elif quadCode == "RETURN":
                a1 = int(quad[1])
                a3 = int(quad[3])
                self.memSeg(a3).setValue(a3, self.memSeg(a1).getValue(a1))
                # Free memory from the previous context
                self.memUsage -= self._localMemory[-1].memSize - self._tempMemory[-1].memSize
                # Remove the current context and return to the last ip
                self.removeContext()
                ip = self._jumpStack.pop()
            elif quadCode == "ENDFUNC":
                # Free up memory space
                self.memUsage -= self._localMemory[-1].memSize - self._tempMemory[-1].memSize
                # Remove the current context and return to the last ip
                self.removeContext()
                ip = self._jumpStack[-1]
                self._jumpStack.pop()
            # Reading and Writting
            elif quadCode == "PRINT":
                a3 = None
                #print(quad[3][0])
                if quad[3][0] == '\"': 
                    a3 = quad[3]
                    print(a3[1:-1])
                else:
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
                if not(a3 >= 18000 and a3 < 20000):    
                    self.setReadInput(temp, a3)
                else:
                    self.memSeg(a3).setValue(a3, temp)
                self.memUsage += 1
            # Arrays and Matrixes
            # Verify that the parameter is inside the allowed limits
            elif quadCode == "VERIFY":
                a1 = int(quad[1])
                a3 = int(quad[3])
                val1 = self.memSeg(a1).getValue(a1)
                if isinstance(val1, float):
                    print("Indices must be of type \"int\"")
                    return
                limSup = self.memSeg(a3).getValue(a3)
                if not(val1 >= 0 and val1 < limSup):
                    print("Index out of bounds")
                    return
            # Must add the offset to the address and store the value
            elif quadCode == "++":
                a1 = int(quad[1])
                a2 = int(quad[2])
                a3 = int(quad[3])
                # Add contents of a1 to address a2 (Offset address a2)
                a2Offset = self.memSeg(a1).getValue(a1) + a2
                self.memSeg(a3).setValue(a3, a2Offset)
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
                    intSeg = self.memSeg(a3).memType["int"]
                    if a3 >= intSeg and a3 < intSeg + 2000:
                        res = int(res)
                    self.memSeg(a3).setValue(a3, res)
                    self.memUsage += 1
                else:
                    runTimeError = "ERROR division by 0 not supported"
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