from virtualMemory import memoryArchitecture

class Avail:
    # Currently only temporary addresses
    startAddress = None

    def __init__(self):
        self.hardReset()

    def next(self, addressType):
        typeAvail = self.address[addressType]
        self.address[addressType] += 1
        return typeAvail

    def hardReset(self):
        #del(self.address)
        self.address = memoryArchitecture["TS"].copy()

