from ast import operator
from collections import deque

from semanticCube import AtomicType, semantics
from avail import Avail


class Quadruples:
    # Temporary Address Manager
    avail = Avail()

    # List of codes that will be passed to the virtual machine and used in quadruples
    quadCodes = {
        'p' : 'PRINT',
        'r' : 'READ',
        'goF' : 'GOTOF',
        'goT' : 'GOTOT',
        'go' : 'GOTO'
    }

    def resetAvail(self):
        self.avail.hardReset()

    # Operators stack
    operatorStack = deque()
    # Operand stack
    operandStack = deque()
    # Types stack
    typeStack = deque()
    # Jump Stack
    jumpStack = deque()

    # cube = semanticCube()  # Should we create the object here (?)
    quadList = []

    # Instruction Pointer
    ip = 0

    def pushOperandType(self, operand, opType):
        self.operandStack.append(operand)
        self.typeStack.append(opType)

    def pushOperator(self, operator):
        self.operatorStack.append(operator)

    def createQuadruple(self, operator, left_operand=None, right_operand=None, temp=None):
        quadruple = [operator, left_operand, right_operand, temp]
        self.ip += 1
        self.quadList.append(quadruple)
        #print(f'{self.ip - 1}) {self.quadList[-1][0]},\t{self.quadList[-1][1]},\t{self.quadList[-1][2]},\t{self.quadList[-1][3]}')

    # Creates quadruples for expressions and assignment
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
    
    # Creates the quadruple for print and read
    def createPRQuad(self, value, isPrint):
        # If the value is a cte string
        if isPrint:
            code = self.quadCodes['p']
            if value:
                # Change "Print" value to a defined type
                self.createQuadruple(code, None, None, value)
            else:
                # If you have an expression
                exprValue = self.operandStack.pop()  # get the value of the resultant expression
                self.typeStack.pop()
                self.createQuadruple(code, None, None, exprValue)
        else:
            code = self.quadCodes['r']
            exprValue = self.operandStack.pop()  # get the value of the resultant expression
            self.typeStack.pop()
            self.createQuadruple(code, None, None, exprValue)

    def fill(self, quadNum, destination):
        self.quadList[quadNum][3] = destination
        print(self.quadList[quadNum])

    def fillGotos(self):
        quadNum = self.jumpStack.pop()
        self.fill(quadNum, self.ip)

    def createGotoF(self):
        tempType = self.typeStack.pop()
        if tempType == AtomicType.BOOL:
            result = self.operandStack.pop()
            self.createQuadruple(self.quadCodes['goF'], result, None, None)
            self.jumpStack.append(self.ip - 1)
        else:
            print("ERROR: Expected bool result")

    def createGoto(self):
        self.createQuadruple(self.quadCodes['go'])
        quadNum = self.jumpStack.pop()
        self.jumpStack.append(self.ip - 1)
        self.fill(quadNum, self.ip)   

    def addJump(self):
        self.jumpStack.append(self.ip) 

    def __str__(self):
        columns = 3

        index = 0
        formatted = ''
        for quad in self.quadList:
            formatted += f'{index})\t{quad[0]}\t{quad[1]}\t{quad[2]}\t{quad[3]}\t\t'
            index += 1
            if index % columns == 0:
                formatted += '\n'
        
        return formatted
