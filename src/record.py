# Class that manages the dictionaries format
from enum import Enum

class programTypes(str, Enum):
    PROGRAM = "PROGRAM"
    CLASS = "CLASS"
    MAIN = "MAIN"

class Record:
    def __init__(self):
        # has the current parameters of the record
        self.currentRecord = {}

    def setType(self, type):
        self.currentRecord['type'] = type

    def setMemoryAdress(self, address):
        self.currentRecord['address'] = address

    def setQuadNumber(self, quadNum):
        self.currentRecord['quadNum'] = quadNum

    def setChildRef(self, childRef):
        self.currentRecord['childRef'] = childRef

    def getChildRef(self):
        return self.currentRecord['childRef']

    def clearCurrentRecord(self):
        self.currentRecord = {}

    def returnRecord(self):
        return self.currentRecord

    # ProgramTypes getters
    def getProgramType(self):
        return programTypes.PROGRAM.value

    def getClassType(self):
        return programTypes.CLASS.value

    def getMainType(self):
        return programTypes.MAIN.value


if __name__ == '__main__':
    reg = Record()

    reg.setType("int")
    reg.setParentRef("none")
    reg.setChildRef("vars")
    x = reg.returnRecord()
    print(x)

    reg.clearCurrentRecord()
    x = reg.returnRecord()
    print(x)
