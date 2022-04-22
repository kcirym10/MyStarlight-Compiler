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
        self.is_varTable = is_varTable

    def keyNotExists(self, key):
        if key not in self:
            return True
        return False
        
    # Generic for both functions (scopes) and variables
    def saveRecord(self, key, value):
        # Must first if key doesn't exist in current table
        if self.keyNotExists(key):
            self[key] = value
        else:
            # Temporary print, should store in error handler to be reported
            print(f"Multiple declaration of key: \"{key}\"")

    # Search function for the parent tree


if __name__ == "__main__":
    sym = symTable()
    key = "name"
    value1 = ("a", "b", "c")
    value2 = 1
    sym.saveRecord(key, value1)
    sym.saveRecord(key, value2)
    print(sym)