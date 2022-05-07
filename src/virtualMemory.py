import copy

memoryArchitecture = {
    "GS" : { # Global Segment
        "int" : 0,
        "float" : 5000,
        "char" : 10000,
        "bool" : 12000
    },
    "LS" : { # Local Segment
        "int" : 13000,
        "float" : 18000,
        "char" : 23000,
        "bool" : 25000
    },
    "TS" : { # Temporary Segment
        "int" : 27000,
        "float" : 32000,
        "char" : 37000,
        "bool" : 39000
    },
    "CS" : { # Constant Segment
        "int" : 41000,
        "float" : 46000,
        "char" : 51000,
        "bool" : 53000
    }
}

class VirtualMemory:
    memory = None
    def __init__(self):
        self.memory = copy.deepcopy(memoryArchitecture)

    def nextGlobal(self, addressType):
        address = self.memory["GS"][addressType]
        self.memory["GS"][addressType] += 1
        return address

    def nextLocal(self, addressType):
        address = self.memory["LS"][addressType]
        self.memory["LS"][addressType] += 1
        return address

    def resetLocal(self):
        self.memory["LS"] = copy.deepcopy(memoryArchitecture["LS"])

    # def resetTemporary(self):
    #     self.memory["TS"] = dict(memoryArchitecture["TS"])

    # def nextAvail(self, addressType):
    #     address = self.memory["TS"][addressType]
    #     self.memory["TS"][addressType] += 1
    #     return address

    def nextConstant(self, addressType):
        address = self.memory["CS"][addressType]
        self.memory["CS"][addressType] += 1
        return address