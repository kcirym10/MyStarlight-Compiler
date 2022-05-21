from distutils.log import error
from enum import Enum
from helper import errorList


class AtomicType(str, Enum):
    # Operand Types
    INT = "int"
    FLOAT = "float"
    CHAR = "char"  # or string(?)
    BOOL = "bool"


class OperatorType(str, Enum):
    # Operator Types
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    ASSIGN = "="
    GREATER = ">"
    SMALLER = "<"
    GREATER_EQUAL = ">="
    SMALLER_EQUAL = "<="
    EQUALS = "=="
    AND = "&"
    OR = "|"

# Specify the resultant type of an operation


class semanticCube:
    cube = {
        # Operations with INT type
        # first  level dictionary
        AtomicType.INT: {
            # second level dictionary
            AtomicType.INT: {
                OperatorType.ADD: AtomicType.INT,
                OperatorType.SUB: AtomicType.INT,
                OperatorType.MUL: AtomicType.INT,
                OperatorType.DIV: AtomicType.INT,
                OperatorType.ASSIGN: AtomicType.INT,
                OperatorType.GREATER: AtomicType.BOOL,
                OperatorType.SMALLER: AtomicType.BOOL,
                OperatorType.GREATER_EQUAL: AtomicType.BOOL,
                OperatorType.SMALLER_EQUAL: AtomicType.BOOL,
                OperatorType.EQUALS: AtomicType.BOOL
            },
            # second level dictionary
            AtomicType.FLOAT: {
                OperatorType.ADD: AtomicType.FLOAT,
                OperatorType.SUB: AtomicType.FLOAT,
                OperatorType.MUL: AtomicType.FLOAT,
                OperatorType.DIV: AtomicType.FLOAT,
                OperatorType.GREATER: AtomicType.BOOL,
                OperatorType.SMALLER: AtomicType.BOOL,
                OperatorType.GREATER_EQUAL: AtomicType.BOOL,
                OperatorType.SMALLER_EQUAL: AtomicType.BOOL,
                OperatorType.EQUALS: AtomicType.BOOL
            }
        },
        # Operations with float type
        # first level dictionary
        AtomicType.FLOAT: {
            # second level dictionary
            AtomicType.FLOAT: {
                OperatorType.ADD: AtomicType.FLOAT,
                OperatorType.SUB: AtomicType.FLOAT,
                OperatorType.MUL: AtomicType.FLOAT,
                OperatorType.DIV: AtomicType.FLOAT,
                OperatorType.ASSIGN: AtomicType.FLOAT,
                OperatorType.GREATER: AtomicType.BOOL,
                OperatorType.SMALLER: AtomicType.BOOL,
                OperatorType.GREATER_EQUAL: AtomicType.BOOL,
                OperatorType.SMALLER_EQUAL: AtomicType.BOOL,
                OperatorType.EQUALS: AtomicType.BOOL
            },
            # second level dictionary
            AtomicType.INT: {
                OperatorType.ADD: AtomicType.FLOAT,
                OperatorType.SUB: AtomicType.FLOAT,
                OperatorType.MUL: AtomicType.FLOAT,
                OperatorType.DIV: AtomicType.FLOAT,
                OperatorType.ASSIGN: AtomicType.FLOAT,
                OperatorType.GREATER: AtomicType.BOOL,
                OperatorType.SMALLER: AtomicType.BOOL,
                OperatorType.GREATER_EQUAL: AtomicType.BOOL,
                OperatorType.SMALLER_EQUAL: AtomicType.BOOL,
                OperatorType.EQUALS: AtomicType.BOOL
            }
        },
        AtomicType.BOOL: {
            AtomicType.BOOL: {
                OperatorType.AND: AtomicType.BOOL,
                OperatorType.OR: AtomicType.BOOL
            }
        }
    }


# Validate if the operation is valid. Get left operand type, right operand type and operator
def semantics(left_type, right_type, operator):
    # Checks if the left type is a key in the first dictionary
    if left_type in semanticCube.cube:
        # Checks if the right type is a key in the second dictionary
        if right_type in semanticCube.cube.get(left_type):
            # gets the values of the second dictionary
            rightDictionary = semanticCube.cube.get(left_type).get(right_type)
            if operator in rightDictionary:
                return rightDictionary[operator]
            else:
                print(f"Invalid operator type: \"{operator}\"")
                errorList.append(f"Invalid right operand type: \"{right_type}\"")
        else:
            print(f"Invalid right operand type: \"{right_type}\"")
            errorList.append(f"Invalid right operand type: \"{right_type}\"")
    else:
        print(f"Invalid left operand type: \"{left_type}\"")
        errorList.append(f"Invalid left operand type: \"{left_type}\"")


if __name__ == "__main__":
    test = semanticCube()

    print(semantics('float', 'int', '+'))
