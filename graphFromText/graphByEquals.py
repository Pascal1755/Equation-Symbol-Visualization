import re

def graphByEquals1(Text):

#    listOfEquations = ["albatross=bluejay+cuckoo", "cuckoo = bluejay+duck",
#                       "duck = egret^9", "bluejay=8", "egret=4", "raven=2*crow"]

    listOfEquations = re.split(r'\n',Text)

    graphOfLeft = dict()
    graphOfRight = dict()
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

            LHS = re.findall(r'\w+', result[0])
            RHS = re.findall(r'\w+', result[1])

            if (LHS and RHS):
                # print("LHS:",LHS," RHS:",RHS," len=[",len(LHS),", ",len(RHS),"]")
                if (LHS[0] not in graphOfLeft):
                    graphOfLeft[LHS[0]] = RHS
                else:
                    graphOfLeft[LHS[0]].append(RHS)
                    raise ValueError('conflicting definition in line:\n' + eq)
                for key in RHS:
                    # print(key,LHS[0])
                    if (key is not None) and (LHS[0] is not None):
                        if (key not in graphOfRight):
                            graphOfRight[key] = [LHS[0]]
                        else:
                            graphOfRight[key].append(LHS[0])
            else:
                raise ValueError('incomplete equation expression found in line:\n' + eq)
        else:
            raise ValueError('non-equation expression found in line:\n' + eq)

    return graphOfLeft

def graphByEquals2(Text):

#    listOfEquations = ["albatross=bluejay+cuckoo", "cuckoo = bluejay+duck",
#                       "duck = egret^9", "bluejay=8", "egret=4", "raven=2*crow"]

    listOfEquations = re.split(r'\n',Text)

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

            LHS = re.findall(r'\w+', result[0])
            RHS = re.findall(r'\w+', result[1])

            if (LHS and RHS):

                #If there is more than one entry in the LHS, move LHS[1], LHS[2], etc. over
                #to RHS array, leaving LHS[0] alone
                if (len(LHS) > 1):
                    for k in range(1,len(LHS)):
                        RHS.append(LHS[k])
                    del LHS[1:len(LHS)]


                if (LHS[0] not in graphOfLeft):
                    graphOfLeft[LHS[0]] = RHS
                else:
                    graphOfLeft[LHS[0]].append(RHS)
                    inputError=ValueError('conflicting definition in line:\n' + eq)
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

def graphByEquals3(Text):

#    listOfEquations = ["albatross=bluejay+cuckoo", "cuckoo = bluejay+duck",
#                       "duck = egret^9", "bluejay=8", "egret=4", "raven=2*crow"]

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

            LHS = re.findall(r'\w+', result[0])
            RHS = re.findall(r'\w+', result[1])

            if (LHS and RHS):
                # print("LHS:",LHS," RHS:",RHS," len=[",len(LHS),", ",len(RHS),"]")
                #if (LHS[0] not in graphOfLeft):
                #    graphOfLeft[LHS[0]] = RHS
                #else:
                #    graphOfLeft[LHS[0]].append(RHS)
                #    inputError=ValueError('conflicting definition in line:\n' + eq)
                for k, key in enumerate(LHS):
                    if (key not in graphOfLeft):
                        graphOfLeft[key] = RHS
                    else:
                        graphOfLeft[key].append(RHS)
                        inputError=ValueError('conflicting definition in line:\n' + eq)
                    for kk, otherkey in enumerate(LHS):
                        if (key is not None) and (otherkey is not None)\
                            and (key != otherkey)\
                            and (otherkey not in graphOfLeft[key]):
                            graphOfLeft[key].append(otherkey)
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