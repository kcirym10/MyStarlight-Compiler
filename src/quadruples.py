from ast import operator
from collections import deque

from semanticCube import semanticCube


class Quadruples:

    # Operators stack
    pOperators = deque()
    # Operand stack
    pOperands = deque()
    # Types stack
    pTypes = deque()
    cube = semanticCube()  # Should we create the object here (?)
    pQuadruples = deque()

    def pushOperand(self, operand):
        # TODO: use variable to receive a record such as record = symTabMngr.getRecord(operand)
        if(operand != None):  # Here really goes searchSymbolTable(operand) != None
            self.pOperands.append(operand)
            type = 'INT'  # Here really goes symTable.getType(operand)
            self.pTypes.append(type)
        else:
            print("Variable not declared")

    def createQuadruple(self, operator, left_operand, right_operand, temp):
        quadruple = operator + left_operand + right_operand + temp
        self.pQuadruples.append(quadruple)

    def createIfTopIs(self, operator):
        #If operator stack not empty
        if self.pOperators:
            # Check top of the stack
            oper = self.pOperators.pop()
            self.pOperators.append(oper)
            if(oper == operator):
                oper = self.pOperators.pop()
                right_operand = self.pOperands.pop()  # right operand
                left_operand = self.pOperands.pop()  # left operand
                right_type = self.pTypes.pop()
                left_type = self.pTypes.pop()

                # Check the type of the temporal
                tempType = self.cube.semantics(left_type, right_type, operator)
                if(tempType != None):
                    # Assign a memory space to temp
                    temp = 5  # here goes avail(tempType)
                    self.createQuadruple(oper, left_operand, right_operand, temp)
                    # Add the temporal variable to the Operands stack
                    self.pOperands.append(temp)
                else:
                    print("Type Mismatch")
            else:
                self.pOperators.append(operator)
        else:
            self.pOperators.append(operator)
