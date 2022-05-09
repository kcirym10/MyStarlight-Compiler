from ast import operator
from collections import deque

from semanticCube import semantics
from avail import Avail


class Quadruples:
    # Temporary Address Manager
    avail = Avail()

    def resetAvail(self):
        self.avail.hardReset()

    # Operators stack
    operatorStack = deque()
    # Operand stack
    operandStack = deque()
    # Types stack
    typeStack = deque()
    # cube = semanticCube()  # Should we create the object here (?)
    pQuadruples = deque()

    def pushOperandType(self, operand, opType):
        self.operandStack.append(operand)
        self.typeStack.append(opType)

    def pushOperator(self, operator):
        self.operatorStack.append(operator)

    def createQuadruple(self, operator, left_operand=None, right_operand=None, temp=None):
        quadruple = (operator, left_operand, right_operand, temp)
        self.pQuadruples.append(quadruple)
        print(
            f'{self.pQuadruples[-1][0]},\t{self.pQuadruples[-1][1]},\t{self.pQuadruples[-1][2]},\t{self.pQuadruples[-1][3]}')

    def createIfTopIs(self, operator):
        # If operator stack not empty
        if self.operatorStack:
            # Check top of the stack
            oper = self.operatorStack.pop()
            self.operatorStack.append(oper)
            # print("In create")
            if(oper in operator):
                # print(oper)
                oper = self.operatorStack.pop()
                # self.operatorStack.append(oper)
                #print("Operator: ", oper)
                right_operand = self.operandStack.pop()  # right operand
                left_operand = self.operandStack.pop()  # left operand
                right_type = self.typeStack.pop()
                left_type = self.typeStack.pop()

                # TODO: Implement Avail class. Must push new avail to operandStack and new type to typeStack
                # Check the type of the temporal
                tempType = semantics(left_type, right_type, oper)
                #print("TEMP TYPE: ",tempType)
                if(tempType != None):
                    if oper == '=':
                        self.createQuadruple(
                            oper, right_operand, None, left_operand)
                    else:
                        # Assign a memory space to temp
                        temp = self.avail.next(tempType)
                        self.createQuadruple(
                            oper, left_operand, right_operand, temp)
                        # Add the temporal variable to the Operands stack
                        self.operandStack.append(temp)
                        self.typeStack.append(tempType)
                else:
                    print("Type Mismatch")

    def createPRQuad(self, value, isPrint):
        # If the value is a cte string
        if isPrint:
            if value:
                # Change "Print" value to a defined type
                self.createQuadruple("PRINT", None, None, value)
            else:
                # If you have an expression
                exprValue = self.operandStack.pop()  # get the value of the resultant expression
                self.typeStack.pop()
                self.createQuadruple("PRINT", None, None, exprValue)
        else:
            exprValue = self.operandStack.pop()  # get the value of the resultant expression
            self.typeStack.pop()
            self.createQuadruple("READ", None, None, exprValue)
