# Class that manages the dictionaries format

class Register:

    def __init__(self):
        self.mainDict = {}  # create an empty dictionary

    # Function that adds the global parameters of the program to the main dictionary
    def addGlobalDic(self, name, type, parentRef, childRef):
        self.parentRef = None  # ensures that the global parameters cannot have parent reference
        # set the parameters to a list
        params = [type, self.parentRef, childRef]
        # adds a new register to the dictionary with name as key and params as a list of values
        self.mainDict[str(name)] = str(params)

    # Function that returns the main dictionary
    def returnDict(self):
        return self.mainDict


if __name__ == '__main__':
    reg = Register()

    reg.addGlobalDic('patito', 'program', 'dad', 'vars')
    reg.addGlobalDic('save', 'func', 'program', 'varsSave')
    x = reg.returnDict()
    print(x)
