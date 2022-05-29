import copy

# memoryArchitecture = {
#     "GS" : { # Global Segment
#         "int" : 0,
#         "float" : 5000,
#         "char" : 10000
#     },
#     "LS" : { # Local Segment
#         "int" : 12000,
#         "float" : 17000,
#         "char" : 22000
#     },
#     "TS" : { # Temporary Segment
#         "int" : 24000,
#         "float" : 29000,
#         "bool" : 34000
#     },
#     "CS" : { # Constant Segment
#         "int" : 36000,
#         "float" : 41000,
#         "char" : 46000
#     }
# }

memoryArchitecture = {
    "GS" : { # Global Segment
        "int" : 0,
        "float" : 2000,
        "char" : 4000
    },
    "LS" : { # Local Segment
        "int" : 6000,
        "float" : 8000,
        "char" : 10000
    },
    "TS" : { # Temporary Segment
        "int" : 12000,
        "float" : 14000,
        "bool" : 16000
    },
    "CS" : { # Constant Segment
        "int" : 18000,
        "float" : 20000,
        "char" : 22000
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

    def resetAvail(self):
        self.memory["TS"] = dict(memoryArchitecture["TS"])

    def nextAvail(self, addressType):
        address = self.memory["TS"][addressType]
        self.memory["TS"][addressType] += 1
        return address

    # Returns the local count variables that were used in a list
    def getLocalSize(self):
        mls = self.memory["LS"]
        mals = memoryArchitecture["LS"]
        return [
                    mls["int"] - mals["int"],
                    mls["float"] - mals["float"],
                    mls["char"] - mals["char"]
                ]

    # Returns the local count of temporals that were used in a list
    def getTempSize(self):
        mts = self.memory["TS"]
        mats = memoryArchitecture["TS"]
        return [
                    mts["int"] - mats["int"],
                    mts["float"] - mats["float"],
                    mts["bool"] - mats["bool"]
                ]

    def nextConstant(self, addressType):
        address = self.memory["CS"][addressType]
        self.memory["CS"][addressType] += 1
        return address