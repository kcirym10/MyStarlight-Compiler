from ast import operator
from collections import deque
from distutils.log import error
from re import I

from compiler.semanticCube import AtomicType, semantics
from compiler.virtualMemory import VirtualMemory
from compiler.helper import errorList


class Quadruples:
    # Temporary Address Manager
    avail = VirtualMemory()

    # List of codes that will be passed to the virtual machine and used in quadruples
    quadCodes = {
        'p' : 'PRINT',
        'r' : 'READ',
        'goF' : 'GOTOF',
        'goT' : 'GOTOT',
        'go' : 'GOTO',
        'ef' : 'ENDFUNC',
        'era' : 'ERA',
        'param' : 'PARAM',
        'goSub' : 'GOSUB',
        'ep' : 'ENDPROGRAM',
        'return' : 'RETURN',
        'ver' : 'VERIFY'
    }

    def resetAvail(self):
        self.avail.resetAvail()

    # Operators stack
    operatorStack = deque()
    # Operand stack
    operandStack = deque()
    # Types stack
    typeStack = deque()
    # Jump Stack
    jumpStack = deque()
    # Dimension Stack
    dimStack = deque()

    # cube = semanticCube()  # Should we create the object here (?)
    quadList = []

    # Instruction Pointer
    ip = 0
    # Param Pointer
    currentSignature = []
    sigIndex = [0]

    def pushOperandType(self, operand, opType):
        if len(errorList) == 0:
            self.operandStack.append(operand)
            self.typeStack.append(opType)

    def pushOperator(self, operator):
        if len(errorList) == 0:
            self.operatorStack.append(operator)

    def createQuadruple(self, operator, left_operand=None, right_operand=None, temp=None):
        if len(errorList) == 0:
            quadruple = [operator, left_operand, right_operand, temp]
            self.ip += 1
            self.quadList.append(quadruple)
        #print(f'{self.ip - 1}) {self.quadList[-1][0]},\t{self.quadList[-1][1]},\t{self.quadList[-1][2]},\t{self.quadList[-1][3]}')

    # Creates quadruples for expressions and assignment
    def createIfTopIs(self, operator):
        if len(errorList) == 0:
            # If operator stack not empty
            if len(self.operatorStack) > 0:
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
                    if len(self.operandStack) >= 1:
                        left_operand = self.operandStack.pop()  # left operand
                    else:
                        errorList.append("Expression error, posible assignment of void function")
                        return
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
                            temp = self.avail.nextAvail(tempType)
                            self.createQuadruple(
                                oper, left_operand, right_operand, temp)
                            # Add the temporal variable to the Operands stack
                            self.operandStack.append(temp)
                            self.typeStack.append(tempType)
                    else:
                        print("Type Mismatch")
                        errorList.append("Type Mismatch")
    
    # Creates the quadruple for print and read
    def createPRQuad(self, value, isPrint):
        if len(errorList) == 0:
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

    # Modifies the actual structure holding the goto destination
    def fill(self, quadNum, destination):
        if len(errorList) == 0:
            self.quadList[quadNum][3] = destination

    # Fills the goto at the jumpStack's quadNum
    def fillGotos(self):
        if len(errorList) == 0:
            quadNum = self.jumpStack.pop()
            self.fill(quadNum, self.ip)

    # Creates a gotoF for regular working expressions such as ifs and whiles
    # Note: does not work for a traditional do-while
    def createGotoF(self):  
        if len(errorList) == 0:
            tempType = self.typeStack.pop()
            if tempType == AtomicType.BOOL:
                result = self.operandStack.pop()
                self.createQuadruple(self.quadCodes['goF'], result, None, None)
                self.jumpStack.append(self.ip - 1)
            else:
                print("ERROR: Expected bool result")
                errorList.append("ERROR: Expected bool result")

    # Creates first goto quadruple and saves the quadNum to the jumpStack
    def createGotoMain(self):
        if len(errorList) == 0:
            self.createQuadruple(self.quadCodes['go'], None, None, None)
            self.jumpStack.append(self.ip - 1)

    # Creates a goto for an if statement which saves its quadNum for when the else part ends
    def createGoto(self):
        if len(errorList) == 0:
            self.createQuadruple(self.quadCodes['go'])
            quadNum = self.jumpStack.pop()
            self.jumpStack.append(self.ip - 1)
            self.fill(quadNum, self.ip)

    # The while goto fills the gotoF, then fills the newly generated goto which returns to the while expression
    def createWhileGoto(self):
        if len(errorList) == 0:
            self.createQuadruple(self.quadCodes['go'])
            quadNum = self.jumpStack.pop()
            self.fill(quadNum, self.ip)
            quadNum = self.ip - 1
            dest = self.jumpStack.pop()
            self.fill(quadNum, dest)

    # Adds current ip to the jumpStack
    def addJump(self):
        if len(errorList) == 0:
            self.jumpStack.append(self.ip) 

    def createEndFunc(self):
        if len(errorList) == 0:
            self.createQuadruple(self.quadCodes['ef'], None, None, None)

    def createERA(self, funcSize, funcSig):
        if len(errorList) == 0:
            self.createQuadruple(self.quadCodes['era'], None, None, funcSize)
            # Initialize param pointer to 0 and save current function signature
            self.sigIndex.append(0)
            self.currentSignature.append(funcSig)

    def createParam(self):
        if len(errorList) == 0:
            if self.sigIndex[-1] < len(self.currentSignature[-1]):
                arg = self.operandStack.pop()
                argType = self.typeStack.pop()
                currentParam = self.currentSignature[-1][self.sigIndex[-1]]
                if argType == currentParam[0]:
                    self.createQuadruple(self.quadCodes['param'], arg, None, currentParam[1])
                else:
                    errorList.append(f"Type Mismatch in function call: {argType} and {self.currentSignature[-1][self.sigIndex[-1]][0]}")
                    #print(f"Type Mismatch in function call: {argType} and {self.currentSignature[self.sigIndex][0]}")
                
            # else:
            #     errorList.append("Too many parameters")
            #     print("Too many parameters")

            # We increment the counter to receive the next or compare with function signature at the end
            self.sigIndex[-1] += 1

    def createGoSub(self, quadNum):
        if len(errorList) == 0:
            # Verify that the signature's index is the correct length
            if self.sigIndex[-1] == len(self.currentSignature[-1]):
                self.createQuadruple(self.quadCodes['goSub'], None, None, quadNum)
            elif self.sigIndex[-1] < len(self.currentSignature[-1]):
                errorList.append('Too little arguments')
            else:
                errorList.append('Too many arguments')

            self.currentSignature.pop()
            self.sigIndex.pop()
    
    def createEndProgram(self):
        if len(errorList) == 0:
            self.createQuadruple(self.quadCodes['ep'], None, None, None)
    
    def createReturn(self, returnRecord):
        if len(errorList) == 0:
            # First remove the global return address and the result temp
            returnAddress = returnRecord['address']
            returnType = returnRecord['type']
            result = self.operandStack.pop()
            resultType = self.typeStack.pop()
            self.createQuadruple(self.quadCodes['return'], result, None, returnAddress)
            # Then return the global address which received the result to the stack
            # This address will be assigned to a temporal address created on function call
            # self.pushOperandType(returnAddress, returnType)

    def createReturnAssignment(self, returnRecord):
        if len(errorList) == 0:
            print(self.operandStack)
            # First remove the return address from the stack
            returnAddress = returnRecord['address']
            returnType = returnRecord['type']
            # Then create a new temporal space to assign the address to
            result = self.avail.nextAvail(returnType)
            resultType = returnType
            # Now add the returns global address to the temporal address
            self.createQuadruple('=', returnAddress, None, result)
            # Finally return the temporal address to the stack
            self.pushOperandType(result, resultType)
            print(self.operandStack)

    # Arrays
    def pushDim(self, dim):
        if len(errorList) == 0:
            self.dimStack.append(dim)

    def createVerify(self, dimNum = 0):
        if len(errorList) == 0:
            # Create verify quadruple
            self.createQuadruple(self.quadCodes['ver'], self.operandStack[-1], 0, self.dimStack[-1][0])

            aux = self.operandStack.pop()
            temp = self.avail.nextAvail('int')
            self.createQuadruple('*', aux, self.dimStack[-1][1], temp)
            self.operandStack.append(temp)

            if dimNum > 0:
                aux2 = self.operandStack.pop()
                aux1 = self.operandStack.pop()
                temp = self.avail.nextAvail('int')
                self.createQuadruple('+', aux1, aux2, temp)
                self.operandStack.append(temp)

    def __str__(self):
        if len(errorList) == 0:
            columns = 3

            index = 0
            formatted = ''
            for quad in self.quadList:
                if isinstance(quad[3], list):
                    formatted += f'{index})\t{quad[0]}\t{quad[1]}\t{quad[2]}\t{quad[3]}\t'
                else:
                    formatted += f'{index})\t{quad[0]}\t{quad[1]}\t{quad[2]}\t{quad[3]}\t\t\t'
                index += 1
                if index % columns == 0:
                    formatted += '\n'
            
            return formatted
        else:
            return ""
