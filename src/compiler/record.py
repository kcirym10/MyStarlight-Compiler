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

    # Size structure is :  [[local int, local float, local char], 
    #                       [temp int, temp float, temp bool]]
    def setSizeStruct(self):
        self.currentRecord['size'] = [[0, 0, 0], [0, 0, 0]]

    def setChildRef(self, childRef):
        self.currentRecord['childRef'] = childRef

    def getChildRef(self):
        return self.currentRecord['childRef']

    # Arrays and matrixes
    # Creates the Dim reference to a list of lists formed by dimension limit and m(n)
    def setDimList(self):
        self.currentDim = 0
        self.dimR = 1
        self.currentRecord['dims'] = [[]]
    
    def setDimLim(self, dimLim):
        # Creates a new node
        if self.currentDim > 0:
            self.currentRecord['dims'].append([])

        # Appends the upper limit to the node and calculates the new R
        self.currentRecord['dims'][self.currentDim].append(dimLim)
        self.dimR = (dimLim) * self.dimR
    
    def incDimCount(self):
        self.currentDim += 1

    def calcDimMs(self):
        # print(self.currentDim)
        # print(self.currentRecord['dims'])
        # Calculate and store m for each dimension
        for dim in self.currentRecord['dims']:
            # Sets to 1 and keeps compiling searching for new errors
            if (dim[0] == 0):
                dim[0] = 1
            mDim = int(self.dimR / (dim[0]))
            dim.append(mDim)
            self.dimR = mDim

        # print(print(self.currentRecord['dims']))
        # End of array reset dimension and r
        self.currentDim = 0
        self.dimR = 1

    def clearCurrentRecord(self):
        self.currentRecord = {}

    # Used for arrays and matrices in order to update the current record
    def setCurrentRecord(self, record):
        self.currentRecord = record

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
