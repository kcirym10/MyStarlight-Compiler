from typing import Dict
from helper import errorList


'''
    A Symbol Table contains its own scope's reference declarations as well as
    an optional variables table. The scope's references are those of function
    names, the program name or any other function-like declaration.
'''
class symTable(Dict):
    scopeLevel = 0 # Class attribute might change
    def __init__(self, parentRef = None, parentName = ""):
        self.parentRef = parentRef # Allows for searches into the parent tree
        self.parentName = parentName
    
    def hasVarTable(self):
        if 'VARS' in self:
            return True
        
        return False

    def keyNotExists(self, key):
        if key not in self:
            return True
        return False
    
    def getFuncRecord(self, key):
        if key in self:
            return self[key]
        return None

    def varKeyNotExists(self, key):
        if key not in self['VARS']['childRef']:
            return True
        return False

    def getVarRecord(self, key):
        if key in self['VARS']['childRef']:
            return self['VARS']['childRef'][key]
        return None
        
    # Generic for both functions (scopes) and variables
    def saveRecord(self, key, value):
        # Must first if key doesn't exist in current table
        if self.keyNotExists(key):
            self[key] = value

    def saveVarRecord(self, key, value):
        if self.varKeyNotExists(key):
            self['VARS']['childRef'][key] = value
            return True
        else:
            print(f"Multiple declaration of var key: \"{key}\"")
            errorList.append(f"Multiple declaration of var key: \"{key}\"")
            return False

    # Adds types to function signature
    def addToSignature(self, paramType):
        if 'paramSignature' not in self:
            self['paramSignature'] = [paramType]
        else:
            self['paramSignature'].append(paramType)

    # Search function for the parent tree
    def searchKey(self, key):
        if self.hasVarTable() and not self.varKeyNotExists(key):
            return self.getVarRecord(key)
        return self.search(key, self.parentRef)
    
    def search(self, key, table):
        if table: 
            if table.keyNotExists(key):
                if table.varKeyNotExists(key):
                    return self.search(key, table.parentRef)
                else:
                    return table.getVarRecord(key)
            else:
                return table.getFuncRecord(key)
        return None


    

if __name__ == "__main__":
    sym = symTable()
    key = "name"
    value1 = ("a", "b", "c")
    value2 = 1
    sym.saveRecord(key, value1)
    sym.saveRecord(key, value2)
    print(sym)