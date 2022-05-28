import os

errorList = []

def run():
    file = open(os.path.join(os.path.dirname(__file__), '..', 'out.obejota'))
    line = file.readline()
    while line != "":
        print(line)
        line = file.readline()

def constantFormat(constant):
    return constant[0] + ' ' + str(constant[1]) + '\n'

def quadFormat(quad):
    if isinstance(quad[3], list):
        return(f'{quad[0]}\t{quad[1]}\t{quad[2]}\t{quad[3][0][0]} {quad[3][0][1]} {quad[3][0][2]} {quad[3][1][0]} {quad[3][1][1]} {quad[3][1][2]}\n')
    else:
        return(f'{quad[0]}\t{quad[1]}\t{quad[2]}\t{quad[3]}\n')

def fileWritter(constants, quads):
    filePath = os.path.join(os.path.dirname(__file__), '..', 'out.obejota')
    #filePath = 'out.obejota'

    f = open(filePath, 'w')

    if len(errorList) == 0:
        if constants is not None:
            f.write(str(len(constants)-1)+'\n')
            for key, value in constants.items():
                constant = [key, value]
                f.write(constantFormat(constant))
        else:
            f.write("0\n")
        for quad in quads.quadList:
            f.write(quadFormat(quad))

    f.close()

if __name__ == '__main__':
    run()