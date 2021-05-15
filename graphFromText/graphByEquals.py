import re
from graphFromText.fxnFromText.fxnGraph import getSymbolGraphMulti

##################### Will map x + y = z + u as {'x':['z','u','y']} ##########################
def graphByEquals2(Text):

    #"tokenize" or parse according to newline character, \n
    listOfEquations = re.split(r'\n',Text)

    # strip whitespace, remove tabs and remove blank entries
    for k, eq in enumerate(listOfEquations):
        eq.strip()
        eq.replace("\t","")
        listOfEquations[k]= eq.replace(" ","")
    while ('' in listOfEquations):
        listOfEquations.remove('')

    #### Create a graphOfLeft and a graphOfRight based upon the equations in listOfEquations ####
    #
    #The graphOfLeft will make all symbols on the right hand side point to the left hand symbol
    #The graphOfRight will do the opposite and the left hand symbol will point to all right
    #hand symbols.
    #
    #An example:
    #From the equation a=b+c, the graphOfLeft would have 'a':['b','c']. This would be
    #interpreted as 'b' and 'c' affect 'a'. The graphOfRight would be 'b':['a'] and 'c':['a'].
    #This would be interpreted as 'a' depends upon 'b' and also 'a' depends upon 'c'.

    graphOfLeft = dict()
    graphOfRight = dict()
    inputError=None
    for k, eq in enumerate(listOfEquations):

        result = re.split(r'={1}', eq)  # split into LHS and RHS by exactly one equals sign

        # Left Hand Side (LHS) is every word to the left of exactly one equals sign
        # Right Hand Side (RHS) is every word to the right of exactly one equals sign
        # print("LHS:",result[0]," RHS:",result[1]," len=",len(result))

        # if there is a LHS and RHS, then it is an assignment or equation. Otherwise, it is not.
        # Also, filter out the cases where a <= or >= is found in the result
        if (len(result) == 2 and result[0].find("<") == -1 \
                and result[0].find(">") == -1 and result[1].find("<") == -1 \
                and result[1].find(">") == -1):

            #LHS = re.findall(r'\w+', result[0])
            #RHS = re.findall(r'\w+', result[1])
            foundLeft = re.findall(r'\w+', result[0])
            LHS=[]
            for expr in foundLeft:
                leftMatch = re.match(r'^[a-zA-Z]+[0-9a-zA-Z_]*',expr)
                if (leftMatch is None \
                        and re.match(r'^[0-9]+[a-zA-Z_]+', expr) is not None):
                    inputError = ValueError('\nillegal expression:\n' + expr)
                elif (leftMatch is not None):
                    LHS.append(leftMatch.group(0))

            foundRight = re.findall(r'\w+', result[1])
            RHS=[]
            for expr in foundRight:
                rightMatch = re.match(r'^[a-zA-Z]+[0-9a-zA-Z_]*',expr)
                if (rightMatch is None \
                        and re.match(r'^[0-9]+[a-zA-Z_]+', expr) is not None):
                    inputError = ValueError('\nillegal expression:\n' + expr)
                elif (rightMatch is not None):
                    RHS.append(rightMatch.group(0))

            ###### special case for numbers only on RHS ######
            if ( len(result[1]) != 0 and len(RHS) == 0 ):
                crazy = r'[+-]?\d+\.?\d*[eE][+-]?\d+|[-]?\d+\.\d+|[-]?\d+'
                numberMatch = re.findall(crazy, result[1])
                if (len(numberMatch) != 0):
                    for expr in numberMatch:
                        RHS.append(expr)

            if (LHS and RHS):

                #If there is more than one entry in the LHS, move LHS[1], LHS[2], etc. over
                #to RHS array, leaving LHS[0] alone
                if (len(LHS) > 1):
                    for k in range(1,len(LHS)):
                        RHS.append(LHS[k])
                    del LHS[1:len(LHS)]

                if (LHS[0] not in graphOfLeft):
                    graphOfLeft[LHS[0]] = RHS.copy()
                else:
                    for item in RHS:
                        graphOfLeft[LHS[0]].append(item)
                    inputError=ValueError('\nconflicting definition in line:\n' + eq)
                for key in RHS:
                    # print(key,LHS[0])
                    if (key is not None) and (LHS[0] is not None):
                        if (key not in graphOfRight):
                            graphOfRight[key] = [LHS[0]]
                        else:
                            graphOfRight[key].append(LHS[0])
            else:
                inputError=ValueError('incomplete equation expression found in line:\n' + eq)
        else:
            inputError=ValueError('non-equation expression found in line:\n' + eq)

    return graphOfLeft, inputError

##################### Will map x + y = z + u as {'x':['z','u','y'],'y':['z','u','x']} #####################
def graphByEquals3(Text):

    listOfEquations = re.split(r'\n',Text)

    #strip whitespace and remove blank entries
    # strip whitespace and remove blank entries
    for k, eq in enumerate(listOfEquations):
        listOfEquations[k]= eq.replace(" ","")
        #print(len(listOfEquations[k]))
    while ('' in listOfEquations):
        listOfEquations.remove('')
    #print(listOfEquations)

    graphOfLeft = dict()
    graphOfRight = dict()
    inputError=None
    for k, eq in enumerate(listOfEquations):

        result = re.split(r'={1}', eq)  # split into LHS and RHS by exactly one equals sign

        # Left Hand Side (LHS) is every word to the left of exactly one equals sign
        # Right Hand Side (RHS) is every word to the right of exactly one equals sign
        # print("LHS:",result[0]," RHS:",result[1]," len=",len(result))

        # if there is a LHS and RHS, then it is an assignment or equation. Otherwise, it is not.
        # Also, filter out the cases where a <= or >= is found in the result
        if (len(result) == 2 and result[0].find("<") == -1 \
                and result[0].find(">") == -1 and result[1].find("<") == -1 \
                and result[1].find(">") == -1):

            #LHS = re.findall(r'\w+', result[0])
            #RHS = re.findall(r'\w+', result[1])
            foundLeft = re.findall(r'\w+', result[0])
            LHS=[]
            for expr in foundLeft:
                leftMatch = re.match(r'^[a-zA-Z]+[0-9a-zA-Z_]*',expr)
                if (leftMatch is None \
                        and re.match(r'^[0-9]+[a-zA-Z_]+', expr) is not None):
                    inputError = ValueError('\nillegal expression:\n' + expr)
                elif (leftMatch is not None):
                    LHS.append(leftMatch.group(0))

            foundRight = re.findall(r'\w+', result[1])
            RHS=[]
            for expr in foundRight:
                rightMatch = re.match(r'^[a-zA-Z]+[0-9a-zA-Z_]*',expr)
                if (rightMatch is None \
                        and re.match(r'^[0-9]+[a-zA-Z_]+', expr) is not None):
                    inputError = ValueError('\nillegal expression:\n' + expr)
                elif (rightMatch is not None):
                    RHS.append(rightMatch.group(0))

            ###### special case for numbers only on RHS ######
            if ( len(result[1]) != 0 and len(RHS) == 0 ):
                crazy = r'[+-]?\d+\.?\d*[eE][+-]?\d+|[-]?\d+\.\d+|[-]?\d+'
                numberMatch = re.findall(crazy,result[1])
                if (len(numberMatch) != 0):
                    for expr in numberMatch:
                        RHS.append(expr)

            if (LHS and RHS):
                for k, key in enumerate(LHS):
                    if (key not in graphOfLeft):
                        graphOfLeft[key] = RHS.copy()
                        #print('key = ' + key + ', RHS = ', RHS)
                    else:
                        for item in RHS:
                            if (item not in graphOfLeft[key]):
                                graphOfLeft[key].append(item)
                        #inputError=ValueError('conflicting definition in line:\n' + eq)
                    #print('before adding other left:\n',graphOfLeft)
                    for kk, otherkey in enumerate(LHS):
                        if (key is not None) and (otherkey is not None)\
                            and (key != otherkey)\
                            and (otherkey not in graphOfLeft[key]):
                            #print('key = ' + key + ', otherkey = ' + otherkey)
                            graphOfLeft[key].append(otherkey)
                            #print(graphOfLeft[key])
                            #print('it\'s a multi-expression eq.: ' + key + ',' + otherkey + '\n')
                for key in RHS:
                    # print(key,LHS[0])
                    if (key is not None) and (LHS[0] is not None):
                        if (key not in graphOfRight):
                            graphOfRight[key] = [LHS[0]]
                        else:
                            graphOfRight[key].append(LHS[0])
            else:
                inputError=ValueError('incomplete equation expression found in line:\n' + eq)
        else:
            inputError=ValueError('non-equation expression found in line:\n' + eq)

    return graphOfLeft, inputError

##################### Will map x + y = z + u as {'x':['z','u'],'y':['z','u']} ##########################
def graphByEquals4(Text):

    listOfEquations = re.split(r'\n',Text)

    #strip whitespace and remove blank entries
    #strip whitespace and remove blank entries
    for k, eq in enumerate(listOfEquations):
        listOfEquations[k]= eq.replace(" ","")
        #print(len(listOfEquations[k]))
    while ('' in listOfEquations):
        listOfEquations.remove('')
    #print(listOfEquations)

    graphOfLeft = dict()
    graphOfRight = dict()
    inputError=None
    for k, eq in enumerate(listOfEquations):

        result = re.split(r'={1}', eq)  # split into LHS and RHS by exactly one equals sign

        # Left Hand Side (LHS) is every word to the left of exactly one equals sign
        # Right Hand Side (RHS) is every word to the right of exactly one equals sign
        # print("LHS:",result[0]," RHS:",result[1]," len=",len(result))

        # if there is a LHS and RHS, then it is an assignment or equation. Otherwise, it is not.
        # Also, filter out the cases where a <= or >= is found in the result
        if (len(result) == 2 and result[0].find("<") == -1 \
                and result[0].find(">") == -1 and result[1].find("<") == -1 \
                and result[1].find(">") == -1):

            #LHS = re.findall(r'\w+', result[0])
            #RHS = re.findall(r'\w+', result[1])
            foundLeft = re.findall(r'\w+', result[0])
            LHS=[]
            for expr in foundLeft:
                leftMatch = re.match(r'^[a-zA-Z]+[0-9a-zA-Z_]*',expr)
                if (leftMatch is None \
                        and re.match(r'^[0-9]+[a-zA-Z_]+', expr) is not None):
                    inputError = ValueError('\nillegal expression:\n' + expr)
                elif (leftMatch is not None):
                    LHS.append(leftMatch.group(0))

            foundRight = re.findall(r'\w+', result[1])
            RHS=[]
            for expr in foundRight:
                rightMatch = re.match(r'^[a-zA-Z]+[0-9a-zA-Z_]*',expr)
                if (rightMatch is None \
                        and re.match(r'^[0-9]+[a-zA-Z_]+', expr) is not None):
                    inputError = ValueError('\nillegal expression:\n' + expr)
                elif (rightMatch is not None):
                    RHS.append(rightMatch.group(0))

            ###### special case for numbers only on RHS ######
            if ( len(result[1]) != 0 and len(RHS) == 0 ):
                crazy = r'[+-]?\d+\.?\d*[eE][+-]?\d+|[-]?\d+\.\d+|[-]?\d+'
                numberMatch = re.findall(crazy, result[1])
                if (len(numberMatch) != 0):
                    for expr in numberMatch:
                        RHS.append(expr)

            if (LHS and RHS):
                for k, key in enumerate(LHS):
                    if (key not in graphOfLeft):
                        graphOfLeft[key] = RHS.copy()
                        #print('key = ' + key + ', RHS = ', RHS)
                    else:
                        for item in RHS:
                            if (item not in graphOfLeft[key]):
                                graphOfLeft[key].append(item)
                        #inputError=ValueError('conflicting definition in line:\n' + eq)
                    #print('before adding other left:\n',graphOfLeft)
                    #for kk, otherkey in enumerate(LHS):
                        #if (key is not None) and (otherkey is not None)\
                            #and (key != otherkey)\
                            #and (otherkey not in graphOfLeft[key]):
                            #print('key = ' + key + ', otherkey = ' + otherkey)
                            #graphOfLeft[key].append(otherkey)
                            #print(graphOfLeft[key])
                            #print('it\'s a multi-expression eq.: ' + key + ',' + otherkey + '\n')
                for key in RHS:
                    # print(key,LHS[0])
                    if (key is not None) and (LHS[0] is not None):
                        if (key not in graphOfRight):
                            graphOfRight[key] = [LHS[0]]
                        else:
                            graphOfRight[key].append(LHS[0])
            else:
                inputError=ValueError('incomplete equation expression found in line:\n' + eq)
        else:
            inputError=ValueError('non-equation expression found in line:\n' + eq)

    return graphOfLeft, inputError

##################### Will map z = f(x,y) + u as {'z':['f','u'],'f':['x',y']}, figuratively ###############
##################### Note that the actual graph items are tuples, like ('f',4,'fxn',0,0) #################
##################### The tuples are the following format: (symbolName,character,type,fxnLevel,eqNum) #####
def graphByEqualsFxn1(Text):
    listOfEquations = re.split(r'\n', Text)

    # strip whitespace and remove blank entries
    for k, eq in enumerate(listOfEquations):
        listOfEquations[k] = eq.replace(" ", "")
    while ('' in listOfEquations):
        listOfEquations.remove('')
    # print(listOfEquations)

    inputError = None
    leftHandLinesOfText = []
    rightHandLinesOfText = []
    for k, eq in enumerate(listOfEquations):

        result = re.split(r'={1}', eq)  # split into LHS and RHS by exactly one equals sign

        # Left Hand Side (LHS) is every word to the left of exactly one equals sign
        # Right Hand Side (RHS) is every word to the right of exactly one equals sign
        # print("LHS:",result[0]," RHS:",result[1]," len=",len(result))

        # if there is a LHS and RHS, then it is an assignment or equation. Otherwise, it is not.
        # Also, filter out the cases where a <= or >= is found in the result
        if (len(result) == 2 and result[0].find("<") == -1 \
                and result[0].find(">") == -1 and result[1].find("<") == -1 \
                and result[1].find(">") == -1):

            # LHS = re.findall(r'\w+', result[0])
            # RHS = re.findall(r'\w+', result[1])
            foundLeft = re.findall(r'\w+', result[0])

            for expr in foundLeft:
                leftMatch = re.match(r'^[a-zA-Z]+[0-9a-zA-Z_]*', expr)
                if (leftMatch is None \
                        and re.match(r'^[0-9]+[a-zA-Z_]+', expr) is not None):
                    inputError = ValueError('\nillegal expression:\n' + expr)
                #elif (leftMatch is not None):
                    #LHS.append(leftMatch.group(0))

            foundRight = re.findall(r'\w+', result[1])

            for expr in foundRight:
                rightMatch = re.match(r'^[a-zA-Z]+[0-9a-zA-Z_]*', expr)
                if (rightMatch is None \
                        and re.match(r'^[0-9]+[a-zA-Z_]+', expr) is not None):
                    inputError = ValueError('\nillegal expression:\n' + expr)
                #elif (rightMatch is not None):
                    #RHS.append(rightMatch.group(0))

            ##### check RHS for unbalanced parenthesis #####
            parenCnt = 0
            for char in result[1]:
                if char == '(':
                    parenCnt+=1
                elif char == ')':
                    parenCnt-=1
            if ( parenCnt != 0 ):
                inputError = ValueError('\nunbalanced parenthesis:\n' + eq)
                # issue with error message fix, 4/11/2021
                #inputError = ValueError('\nunbalanced parenthesis:\n' + expr)

            ###### special case for numbers only on RHS ######
            #if (len(result[1]) != 0 and len(RHS) == 0):
                #crazy = r'[+-]?\d+\.?\d*[eE][+-]?\d+|[-]?\d+\.\d+|[-]?\d+'
                #numberMatch = re.findall(crazy, result[1])
                #if (len(numberMatch) != 0):
                    #for expr in numberMatch:
                        #RHS.append(expr)

            if (inputError is None):
                for k, left in enumerate(foundLeft):
                    leftHandLinesOfText.append(left)
                    rightHandLinesOfText.append(result[1])
            #else statement commented out on 4/9/2021
            #else:
                #inputError = ValueError('incomplete equation expression found in line:\n' + eq)
        else:
            inputError = ValueError('non-equation expression found in line:\n' + eq)

    #### LHS and RHS are populated ####
    if (inputError is None):
        symbolGraphMulti = getSymbolGraphMulti(leftHandLinesOfText, rightHandLinesOfText)
    else:
        symbolGraphMulti = dict()

    return symbolGraphMulti, inputError

'''
##################### Will map x + y = z + u as {'x':['z','u'],'y':['z','u']} ##########################
def graphByEquals4(Text):

    listOfEquations = re.split(r'\n',Text)

    #strip whitespace and remove blank entries
    # strip whitespace and remove blank entries
    for k, eq in enumerate(listOfEquations):
        listOfEquations[k]= eq.replace(" ","")
        #print(len(listOfEquations[k]))
    while ('' in listOfEquations):
        listOfEquations.remove('')
    #print(listOfEquations)

    graphOfLeft = dict()
    graphOfRight = dict()
    inputError=None
    for k, eq in enumerate(listOfEquations):

        result = re.split(r'={1}', eq)  # split into LHS and RHS by exactly one equals sign

        # Left Hand Side (LHS) is every word to the left of exactly one equals sign
        # Right Hand Side (RHS) is every word to the right of exactly one equals sign
        # print("LHS:",result[0]," RHS:",result[1]," len=",len(result))

        # if there is a LHS and RHS, then it is an assignment or equation. Otherwise, it is not.
        # Also, filter out the cases where a <= or >= is found in the result
        if (len(result) == 2 and result[0].find("<") == -1 \
                and result[0].find(">") == -1 and result[1].find("<") == -1 \
                and result[1].find(">") == -1):

            #LHS = re.findall(r'\w+', result[0])
            #RHS = re.findall(r'\w+', result[1])
            foundLeft = re.findall(r'\w+', result[0])
            LHS=[]
            for expr in foundLeft:
                leftMatch = re.match(r'^[a-zA-Z]+[0-9a-zA-Z_]*',expr)
                if (leftMatch is None \
                        and re.match(r'^[0-9]+[a-zA-Z_]+', expr) is not None):
                    inputError = ValueError('\nillegal expression:\n' + expr)
                elif (leftMatch is not None):
                    LHS.append(leftMatch.group(0))
            #### Under development ####
            fxnOnRight=re.search(r'(\w+)\((.*)\)', result[1])
            if (fxnOnRight is not None):
                fxnName = fxnOnRight.groups(0)

            else:
                foundRight = re.findall(r'\w+', result[1])
                RHS=[]
                for expr in foundRight:
                    rightMatch = re.match(r'^[a-zA-Z]+[0-9a-zA-Z_]*',expr)
                    if (rightMatch is None \
                            and re.match(r'^[0-9]+[a-zA-Z_]+', expr) is not None):
                        inputError = ValueError('\nillegal expression:\n' + expr)
                    elif (rightMatch is not None):
                        RHS.append(rightMatch.group(0))

                ###### special case for numbers only on RHS ######
                if ( len(result[1]) != 0 and len(RHS) == 0 ):
                    num_regex = r'[+-]?\d+\.?\d*[eE][+-]?\d+|[-]?\d+\.\d+|[-]?\d+'
                    numberMatch = re.findall(num_regex, result[1])
                    if (len(numberMatch) != 0):
                        for expr in numberMatch:
                            RHS.append(expr)

            if (LHS and RHS):
                for k, key in enumerate(LHS):
                    if (key not in graphOfLeft):
                        graphOfLeft[key] = RHS.copy()
                        #print('key = ' + key + ', RHS = ', RHS)
                    else:
                        for item in RHS:
                            if (item not in graphOfLeft[key]):
                                graphOfLeft[key].append(item)
                        #inputError=ValueError('conflicting definition in line:\n' + eq)
                    #print('before adding other left:\n',graphOfLeft)
                    #for kk, otherkey in enumerate(LHS):
                        #if (key is not None) and (otherkey is not None)\
                            #and (key != otherkey)\
                            #and (otherkey not in graphOfLeft[key]):
                            #print('key = ' + key + ', otherkey = ' + otherkey)
                            #graphOfLeft[key].append(otherkey)
                            #print(graphOfLeft[key])
                            #print('it\'s a multi-expression eq.: ' + key + ',' + otherkey + '\n')
                for key in RHS:
                    # print(key,LHS[0])
                    if (key is not None) and (LHS[0] is not None):
                        if (key not in graphOfRight):
                            graphOfRight[key] = [LHS[0]]
                        else:
                            graphOfRight[key].append(LHS[0])
            else:
                inputError=ValueError('incomplete equation expression found in line:\n' + eq)
        else:
            inputError=ValueError('non-equation expression found in line:\n' + eq)

    return graphOfLeft, inputError
'''