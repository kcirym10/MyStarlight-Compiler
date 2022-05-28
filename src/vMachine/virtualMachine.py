from compiler.helper import structsFromFile

class virtualMachine:
    constants = None
    quadList = None

    # Declare memory structure as mem = []
    

    def runInstructions(self):
        ip = 0
        while (self.quadList[ip][0] != "ENDPROGRAM"):
            quad = self.quadList[ip]
            quadCode = quad[0]
            if quadCode == "GOTO":
                ip = int(quad[3])
                print(ip)
                continue
            ip += 1
        
        print(self.quadList[ip][0])


    def run(self):
        self.constants, self.quadList = structsFromFile()
        print(self.constants)
        self.runInstructions()
