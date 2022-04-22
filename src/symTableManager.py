'''
    This class manages the active symbol/variable table.
    It makes use of a stack to manage the top/active table and is the working interface
    between the translation process.
    This class is dependant of the symTable class
'''

from typing import List
from symTable import symTable

class symTableManager(List):
    currentType = None

    def __init__(self):
        self.pushTable(symTable())

    # Sets current type in case needed xD
    def setCurrentType(self, type):
        self.currentType = type

    # Returns the current type
    def getCurrentType(self):
        return self.currentType

    # Returns a new table to be used either as a new scope or a new variables table
    def getNewSymTable(self):
        newSymTable = symTable(self[-1])
        return newSymTable

    # Pushes a new Symbol Table to the top of the stack
    # this could be a new scope (such as a function) or a vars table
    def pushTable(self, table):
        self.append(table)

    # Inserts a new record into the currently active table at the top
    # of the manager's stack
    def insertRecord(self, key, value):
        self[-1].saveRecord(key, value)

if __name__ == "__main__":
    symMngr = symTableManager()
    key = "Program"
    value1 = {'type': "Program Name", 'pRef': None, 'cRef': None}
    symMngr.insertRecord(key, value1)
    newSymTable = symMngr.getNewSymTable()
    value2 = {'type': "Program Name", 'pRef': symMngr[-1], 'cRef': newSymTable}
    symMngr.pushTable(newSymTable)
    print(symMngr[-1].parentRef)
    symMngr.insertRecord(key, value2)

    print(symMngr)

    # symMngr.insertRecord("key1", '1')
    # symMngr.insertRecord("key2", '2')
    # print(list(symMngr[-1].keys())[-1])