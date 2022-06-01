import sys

from compiler.parser import parseProgram
from compiler.helper import structsFromFile, errorList
from vMachine.virtualMachine import virtualMachine

if __name__ == "__main__":
    opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
    args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

    # Check if arguments were passed along project initialization
    if not args:
        print("Please specify a file to input")
    else:
        fileName = args[0]
        parseProgram(fileName)
        if len(errorList) == 0:
            virtualMachine().run()
        else:
            for err in errorList:
                print(err)
        
        