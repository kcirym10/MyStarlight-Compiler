'''
    This class manages the active symbol/variable table.
    It makes use of a stack to manage the top/active table and is the working interface
    between the translation process.
    This class is dependant of the symTable class
'''

from typing import List
from symTable import symTable

class symTableManager(List):
    def __init__(self):
        self.pushTable(symTable())

    # Returns a new table to be used either as a new scope or a new variables table
    def getNewSymTable(self):
        return symTable()

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
    newSymTable = symTable()
    value2 = {'type': "Program Name", 'pRef': symMngr[-1], 'cRef': newSymTable}
    symMngr.pushTable(newSymTable)
    symMngr.insertRecord(key, value2)

    print(symMngr)