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

    def pushTable(self, table):
        self.append(table)

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