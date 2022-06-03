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
        return(f'{quad[0]}\t{quad[1]}\t{quad[2]}\t{quad[3][0][0]} {quad[3][0][1]} '+
                 f'{quad[3][0][2]} {quad[3][1][0]} {quad[3][1][1]} {quad[3][1][2]}\n')
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

def structsFromFile():
    file = open(os.path.join(os.path.dirname(__file__), '..', 'out.obejota'))
    line = file.readline()
    constCount = int(line)
    counter = 0
    line = file.readline()
    constants = {}
    quadList = []
    while line != "":
        # Read the ammount of constants and save them to a dict
        if counter <= constCount:
            index = line.find(' ')
            if int(line[index + 1:-1]) >=  22000:
                constants[line[index + 1:-1]] = line[0]
            elif line[:index].find('.') == -1:
                constants[line[index + 1:-1]] = int(line[:index])
            else:
                constants[line[index + 1:-1]] = float(line[:index])

        # This is where constants have finished and quadruples must be processed
        else:
            lineLen = len(line)
            index1 = line.find('\t')
            index2 = line.find('\t', index1 + 1)
            index3 = line.find('\t', index2 + 1)
            quadList.append([line[:index1], line[index1 + 1: index2], line[index2 + 1: index3], line[index3 + 1: -1]])
        line = file.readline()
        counter += 1
    file.close()
    
    return constants, quadList

if __name__ == '__main__':
    run()