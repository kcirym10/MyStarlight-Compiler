from typing import Dict


'''
    A Symbol Table contains its own scope's reference declarations as well as
    an optional variables table. The scope's references are those of function
    names, the program name or any other function-like declaration.
'''
class symTable(Dict):
    scopeLevel = 0 # Class attribute might change
    def __init__(self, parentRef = None, is_varTable = False):
        print("New Symbol Table") 
        self.parentRef = parentRef # Allows for searches into the parent tree
    
    def hasVarTable(self):
        if 'VARS' in self:
            return True
        
        return False

    def keyNotExists(self, key):
        if key not in self:
            return True
        return False

    def varKeyNotExists(self, key):
        if key not in self['VARS']['childRef']:
            return True
        return False
        
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
            return False

    '''# Search function for the parent tree
    def searchKey(self, key):
        if self.getTableType(): # If table is a Vars Table
            if self.keyNotExists:
                return self.searchParentTree(self.parentRef, key)
            print(self[key])
            return self[key]

    def searchForVar(self, table, key):
        if 'VARS' in table:
            if key in table['VARS']['childRef']:
                print('KEY FOUND!',table['VARS']['childRef'][key])
                return table['VARS']['childRef'][key]

        return None

    def searchParentTree(self, table, key):
        if table is not None:
            record = self.searchForVar(table, key)
            if record is not None:
                 return record
            print(self)

            return self.searchParentTree(table.parentRef, key)
            
        return None # Did not find key'''

if __name__ == "__main__":
    sym = symTable()
    key = "name"
    value1 = ("a", "b", "c")
    value2 = 1
    sym.saveRecord(key, value1)
    sym.saveRecord(key, value2)
    print(sym)