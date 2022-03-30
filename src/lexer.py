from sly import Lexer
import re

class StartlightLexer(Lexer):
    # The set of token names specified in all-caps
    # Required set
    tokens = {
        PROGRAM, ID, CLASS_ID, VAR, INT, FLOAT, CHAR, VOID, CLASS, DERIVES, METHODS, 
        FUNC, RETURN, PRINT, READ, IF, ELSE, WHILE, FOR, TO, MAIN, 
        LESS_OR_EQUAL_TO, GREATER_OR_EQUAL_TO, EQUAL_TO, CTE_INT, CTE_FLOAT, CTE_CHAR,
        CTE_STRING
            }

    # The set of literal characters formed by a single character
    # Optional set, but handy
    literals = {
        ';', '[', ']', ',', '(', ')', ':', '{', '}', '=', '.', '|', 
        '&', '<', '>', '+', '-', '*', '/'
        }

    # Expression ignoring rules
    # Ignore rule for spaces
    ignore = r' \t'
    # Ignoring other patterns
    ignore_newline = r'\n+'

    
    # Constant char matching
    CTE_CHAR = r"'\w'"
    # Constant string matching
    CTE_STRING = r'"[\w: ]*"' # Needs revision because matches everything

    # Special class ID rule
    CLASS_ID = r'[A-Z]\w*'

    # General ID match rule
    ID = r'[a-z]\w*'

    # Character Remapping
    # Special cases for ID's (reserved words and types)
    ID['program'] = PROGRAM
    ID['var'] = VAR
    ID['int'] = INT
    ID['float'] = FLOAT
    ID['char'] = CHAR
    ID['void'] = VOID
    ID['class'] = CLASS
    ID['derives'] = DERIVES
    ID['methods'] = METHODS
    ID['func'] = FUNC
    ID['return'] = RETURN
    ID['print'] = PRINT
    ID['read'] = READ
    ID['if'] = IF 
    ID['else'] = ELSE
    ID['while'] = WHILE
    ID['for'] = FOR
    ID['to'] = TO
    ID['main'] = MAIN

    # Function rule matching
    # Rule match for floating point numbers
    # Converts the pattern to a float
    @_(r'[0-9]+\.[0-9]+')
    def CTE_FLOAT(self, t):
        t.value = float(t.value)
        return t
    
    # Rule match for integer numbers
    # Converts the pattern to integer
    @_(r'[0-9]+')
    def CTE_INT(self, t):
        t.value = int(t.value)
        return t


    # Simple Error Handling (maybe resynchronizing?)
    # This method handles lexical errors, reporting them "on screen"
    # and moving on to the next token.
    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

# Only executes when the main code running is the lexer file
# good for simple unit testing
if __name__ == '__main__':
    # Sample input string containig all possible tokens
    data = '''
        program try;
        var
            int i, j;
            char c[10];
            Car car1, car2;
        class Vehicle{
            var
                int size;
            methods:
                func void setSize(int newSize){
                    size = newSize;
                }
        }

        class Car derives Vehicle{}

        func float arithmetic(){
            return ((car.size + 10) - 100/50 * 2);
        }

        func float recursiveSumUntilZero(int x){
            if (x == 0){
                return 0;
            }

            return x + recursiveSumUntilZero(x - 1));
        }

        func void callWithNewSize(int x){
            car1.setSize(x);
        }

        main()
        int inputSize, inputCount;
        {
            print("Enter number of car sizes: ");
            read(inputCount);

            for (i = 0 to 9){
                c[i] = 'c'
            }

            for (i = 0 to inputCount){
                print("Size: ");
                read(inputSize);
                callWithNewSize(inputSize);
                car2.setSize(inputSize);
                print("Car 1 size ", car1.size, "Car 2 size ", car2.size);
            }

            j = 10;
            while (j > 0){
                print("Sum of ", j, " is ", recursiveSumUntilZero(j));
            }
        }
    '''

    lexer = StartlightLexer()
    for token in lexer.tokenize(data):
        print('type = %r, value=%r' %(token.type, token.value))