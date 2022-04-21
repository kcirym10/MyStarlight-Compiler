# Class that manages the dictionaries format

class Record:

    def __init__(self):
        # has the current parameters of the record
        self.currentRecord = {'type': None,
                              'parentRef': None, 'childRef': None}

    def setType(self, type):
        self.currentRecord['type'] = str(type)

    def setParentRef(self, parentRef):
        self.currentRecord['parentRef'] = parentRef

    def setChildRef(self, childRef):
        self.currentRecord['childRef'] = childRef

    def getParentRef(self):
        return self.currentRecord['parentRef']

    def getChildRef(self):
        return self.currentRecord['childRef']

    def clearCurrentRecord(self):
        self.currentRecord = {'type': None,
                              'parentRef': None, 'childRef': None}

    def returnRecord(self):
        return self.currentRecord


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
