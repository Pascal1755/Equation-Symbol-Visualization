'''
The getParenLvl3() parses through a text which has parenthesis
and determines the grouping of characters based upon the number
of parenthesis it has encountered. For instance, if the input
text were as follows:
text = 'x+f(y,z,g(x))'
then the output would be a list of
[0,0,0,0,1,1,1,1,1,1,2,2,2,1]
where the values of list corresponded to the number of parenthesis
encountered for function nesting. The index of the list which was
output directly correlates to the character index in the input text.
Thus, the first 1 value in the list corresponds to the '(' character
after 'f'. The second 1 value in the list corresponds to the 'y'
character. Also, the first 2 value corresponds to the '(' after
'g' and the second 2 value corresponds to the 'x'.
'''
def getParenLvl3(text):
    # Get heirarchical level of parens with fxn considerations
    levelF = []
    fStackHeight = 0
    pStackHeight = 0
    myStack = [] # 'f' for fxn, 'p' for paren
    for k, ch in enumerate(text):
        if (k >= 1 and ch == "(" \
                and text[k-1].isalnum()): #WAS text[k-1].isalpha()
            fStackHeight += 1
            myStack.append('f')  # push 'f' onto stack for fxn
            levelF.append(fStackHeight)
        elif ( ch == "(" ):
            levelF.append(fStackHeight)
            pStackHeight += 1
            myStack.append('p')  # push 'p' onto stack for paren
        elif ( ch == ")" ):
            levelF.append(fStackHeight)
            if ( myStack[-1:][0] == 'p'):
                pStackHeight -= 1
            elif ( myStack[-1:][0] == 'f' ):
                fStackHeight -= 1
            del myStack[-1:]  # pop the stack
        else:
            levelF.append(fStackHeight)

    # Get heirarchical level of parens w/o fxn consideration
    levelP = []
    lvl = 0
    for k, ch in enumerate(text):
        if (ch == "("):
            lvl += 1
            levelP.append(lvl)
        elif (ch == ")"):
            levelP.append(lvl)
            lvl -= 1
        else:
            levelP.append(lvl)

    #levelComp = [levelP[k]-levelF[k] for k in range(0,len(levelF))]

    return levelF, levelP

'''
The getFxnLeft() function is intended to return a function name
from a given index (local variable kk1) within text.

This is used in the getSymbolGraph() subroutine.
'''
def getFxnLeft(kk1,text):
    # Marches backward from "(" unitil non alphanumeric
    # characture is found and grabs string.
    kk2=kk1
    N=len(text) #new
    while (kk2 >= 1 and (text[kk2 - 1]).isalnum()):
        kk2 -= 1
    if ( (text[kk2]).isalnum() ):
        fxnName = text[kk2:(kk1+1)]  # must add +1 for python string
    else:
        fxnName = None

    return fxnName

'''
The getSymbolLnR() function increments/decrements an index (local variables
kk1 and kk2) forward and backward through the text string until a given 
pattern emerges which is consistent with a symbol that represents a symbol or a 
number in scientific notation. Note that this is not intended to identify
function names as getFxnLeft() is intended for that purpose.

The getSymbolLnR() is used within getSymbolGraph() functions to identify 
symbol names and move the position of the index (local variable kk1)
forward to the next symbol in the text.
'''
def getSymbolLnR(kk1,text):
    kk2=kk1
    N=len(text) #new
    sciNumNot = ['.','e','E','-','+']
    sciNumNot1 = ['.']#,'e','E'] #for scientific notation
    sciNumNot2 = ['e-','E-','e+','E+'] #for scientific notation
    wordChars = ['_'] #for certain notation, any others to add?
    while (kk2 >= 1 and (text[kk2-1].isalnum() \
                         or (text[kk2-1] in wordChars)) ):
        kk2 -= 1
    if ( (text[kk2]).isalpha() ):
        # The string found by marching backward is alphanumeric
        # Now, must march forward to get the last character
        while ( kk1 < (N-1) and ( text[kk1+1].isalnum() \
                         or (text[kk1+1] in wordChars) ) ):  # new
            kk1 += 1  # new
        symName = text[kk2:(kk1+1)] #have to add +1 for python string
        kk1 += 1
    elif ( (text[kk2]).isnumeric() ):
        # add negative sign if it's there
        if ( kk2 >= 1 and text[kk2 - 1] == '-' ):
            kk2 -= 1
        # The string found by marching backward is numeric
        # Now, must march forward to get the last character
        while ( kk1 < (N-1) and ( (text[kk1 + 1]).isdigit() \
                or (text[kk1+1] in sciNumNot) ) ):  # new
            if ( text[kk1+1].isdigit() or \
                    (text[kk1+1] in sciNumNot1) ):
                kk1 += 1  # new
            elif ( kk1 < (N-1) and \
                   (text[kk1+1:kk1+3] in sciNumNot2) ):
                kk1 += 2
            else:
                break
                #kk1 += 1
        symName = text[kk2:(kk1+1)] #have to add +1 for python string
        kk1 += 1 #move onto the next thing
    else:
        symName = None
        kk1 += 1  # Nothing here, move onto the next one

    return symName, kk1

'''
The getSymbolGraph() uses an input which is a single line of text.
The input text is parsed and organized into an associative data structure
(a python dictionary/general graph data structure) according to a functional 
language representation. It is presumed that the input text is representative 
of the right hand side of the equation. It is also presumed that function
names are post-pended with an open parenthesis. Function
arguments that represent data are found within the parenthesis
after the function names. For instance, if the following equation
was used:
z = x+y + f(x,y)*g(u(x),w(y))
then the input text would be 'x+y + f(x,y)*g(u(x),w(y))' and
the output would be the following python dictionary:
{'###':['x','y','f','g'],'f':['x','y'],
'g':['u','w'],'u':['x'],'w':['y']}
'''
def getSymbolGraph2(text):
    # listOfArgs=[]
    symbolGraph = dict()
    symbolGraph['###'] = []  # populate lowest level which eventually must point to RHS
    symbolsByLevel = dict()
    listOfSymbols = []
    N = len(text)

    # Get paren level, indicated by number of successive "("
    # Also, get funciton level, indicated by number of "<char>(" pattern
    #listOfFxnLvl, listOfParenLvl = getParenLvl2(text)
    listOfFxnLvl, listOfParenLvl = getParenLvl3(text)

    # take difference of Function level, indicated by "<char>(" pattern
    diff_lvl = [listOfFxnLvl[k + 1] - listOfFxnLvl[k] for k in range(0, N-1)]
    #print(listOfFxnLvl)
    #print(diff_lvl)

    # Populate 0 level symbols
    k = 0
    while (k < N):
        # print(text[k],k,listOfFxnLvl[k])
        if (k <= (N - 1) and \
                listOfFxnLvl[k] == 0 and \
                text[k].isalnum()):
            # and not text[k+1].isalnum()
            #
            # lvl0Name, unused = getSymbolByPos(k,text)
            #
            lvl0Name, k = getSymbolLnR(k, text)  # get the symbol and move to next k
            # print(lvl0Name,k)
            # symbolGraph['###'].append((lvl0Name, k))
            symbolGraph['###'].append((lvl0Name, k-1))  # changed 11-12-2020, see above
        else:
            k += 1

    # Populate heirarchy of symbols
    for lvl in range(0, max([max(listOfFxnLvl), 1])):
        ###### find edges of lvl to lvl+1 ######
        # Initialization
        start = 0
        fin = 0
        fxnNames = []
        fxnName = None
        k = 0
        # print(lvl)
        # for k in range(0,N):
        while (k < N):
            #print(lvl, k)
            if (k < (N - 1) and \
                    listOfFxnLvl[k] == lvl and \
                    diff_lvl[k] == 1 and \
                    text[k].isalnum()):
                # fxnName, unused = getSymbolByPos(k,text)
                fxnName = getFxnLeft(k, text)
                # fxnName, unused = getSymbolLnR(k,text)
                # print(fxnName, k)
                start = k
                #k += 1 #new
            #elif (k == (N - 1) or \
            elif ( ( (k <= (N-2) and \
                   listOfFxnLvl[k] == (lvl+1) and \
                   diff_lvl[k] == -1) or \
                     ( k == (N-1) and \
                     listOfFxnLvl[k] == (lvl+1) )
                   ) and \
                  fxnName is not None ): # OR condition added 11-12-2020
                fin = k
                fxnNames.append((fxnName, start, fin))
            k += 1
                # k += 1 #new
            #else:
                #k += 1
        #print(fxnNames)
        ##### grab symbols at level = lvl+1 #####
        for item in fxnNames:
            tempSym = []  # clear temporary symbol list
            fName = item[0]
            start = item[1]
            fin = item[2]
            # print(fin,N,len(diff_lvl))
            k = start
            while (k <= fin):
                if (listOfFxnLvl[k] == (lvl + 1) and \
                        text[k].isalnum()):
                    symName, k = getSymbolLnR(k, text)  # special note: advances k += 1 or more
                    if (symName is not None):
                        tempSym.append((symName, k-1))  # changed from k to k-1, 11-12-2019
                    else:
                        k += 1
                else:
                    k += 1
                # symbolGraph[fName] = tempSym.copy()
                symbolGraph[(fName,start)] = tempSym.copy()  # changed 11-12-2020, see above
        # print(fxnNames)
    return symbolGraph

'''
The getRow() function assigns rows values to a symbol 
based upon some rules. It is used by getRowsByKey()
'''
def getRow(myKey, symbolGraph, rowsByKey, farRow):
    #case 1: no children
    if ( myKey not in symbolGraph \
        and myKey not in rowsByKey ):
        row = farRow
        farRow -= 1
    #case 3: children found, point to minimum
    elif ( myKey in symbolGraph ):
        maxList=[]  # trying to get the maximum of a negative number
        for item in symbolGraph[myKey]:
            if ( item in rowsByKey ):
                maxList.append(rowsByKey[item])
        if (len(maxList) >= 1):
            row = max(maxList)  #trying to get the maximum of a negative number
        else:
            row = farRow  # this shouldn't happen?
    else:
        row = farRow
    return row, farRow

'''
The getRowsByKey() function performs an assignment of symbols 
to vertical rows for plotting purposes. The input is the 
symbolGraph in the form of a dictionary and the output is a 
dictionary where keys are symbols and values are row numbers. 
A stack based data structure pushes symbols onto the stack until
there are no children left, then items on the stack are removed 
and rows are assigned to the symbol.
'''
def getRowsByKey3(symbolGraph):
    rStack = []
    rowsByKey = {}
    row = 0
    lvl = -1
    iter = 0
    # myKey = '###' # old code
    myKey = list(symbolGraph.keys())[0]  # get root of symbolGraph, cast keys to list and get 0th entry
    stackNotEmpty = True
    farRow = 0
    while (stackNotEmpty):
        child = True
        while (child):
            k = 0
            N = len(symbolGraph[myKey])
            # print('myKey = ', myKey[0])
            while (k < N and \
                   symbolGraph[myKey][k] in rowsByKey):
                k += 1
            while ( k < N and \
                  symbolGraph[myKey][k] not in rowsByKey ):
                if ( symbolGraph[myKey][k] in symbolGraph ):
                    rStack.append(symbolGraph[myKey][k])
                k += 1
#            if (k < N and symbolGraph[myKey][k] in symbolGraph):
#                rStack.append(symbolGraph[myKey][k])
#                lvl += 1
#            else:  # no idea why this is here, but it doesn't work if commented out
                #            j = k
                #            while (j < N and \
                #                symbolGraph[myKey][j] not in symbolGraph \
                #                and symbolGraph[myKey][j] not in rowsByKey):
                #                child = False
                #                rStack.append(symbolGraph[myKey][j])
                #                j += 1
            for item in symbolGraph[myKey]:
                if (item not in symbolGraph \
                        and item not in rowsByKey):
                    child = False
                    rStack.append(item)
            if (k < N):
                myKey = symbolGraph[myKey][k]
            else:
                child = False

        #print(rStack, lvl)
        #    noChild = True
        #    while ( noChild ):
        #        rowsByKey[rStack[-1:][0]] = row  # assign row
        #        if ( rStack[-1:][0] in symbolGraph ):
        #            noChild = False
        #        else:
        #            del rStack[-1:]  # pop item
        childRowsWereInStack = True
        moreSymbolsFound = False
        while ( childRowsWereInStack and \
               (not moreSymbolsFound) and \
               len(rStack) > 0):
            #print(rStack[-1:][0], childRowsAssigned, moreSymbolsFound)
            if (rStack[-1:][0] not in symbolGraph):
                # rowsByKey[rStack[-1:][0]] = row  # assign row
                rowsByKey[rStack[-1:][0]], farRow = getRow(rStack[-1:][0],
                                                           symbolGraph,
                                                           rowsByKey,
                                                           farRow)
                del rStack[-1:]  # pop item
            else:
                #            childRowsNotAssigned = True
                #            for item in symbolGraph[rStack[-1:][0]]:
                #                if ( item in rowsByKey ):
                #                    childRowsNotAssigned = False
                #            if ( not childRowsNotAssigned ):
                #                rowsByKey[rStack[-1:][0]] = row
                #                del rStack[-1:]  # pop item
                childRowsWereInStack = True
                for item in symbolGraph[rStack[-1:][0]]:
                    #print(item, (item in symbolGraph))
                    if (item not in rowsByKey and \
                            item not in symbolGraph):
                        childRowsWereInStack = False
                    elif (item not in rowsByKey and \
                          item in symbolGraph):
                        moreSymbolsFound = True
                if (childRowsWereInStack and not moreSymbolsFound):
                    # rowsByKey[rStack[-1:][0]] = row
                    rowsByKey[rStack[-1:][0]], farRow = getRow(rStack[-1:][0],
                                                               symbolGraph,
                                                               rowsByKey,
                                                               farRow)
                    del rStack[-1:]  # pop item

        #print( rStack )
        if (len(rStack) > 0):
            myKey = rStack[-1:][0]
        iter += 1
        stackNotEmpty = (len(rStack) > 0 and iter <= 200)
    # print(stackNotEmpty)
    return rowsByKey

'''
New addition to establish "dominant symbols" if a symbol is on more
than one line of code. For instance...
x = f(x,y,z)  #updates x
w = 7*x + 2*y  #uses the updated value of x
Note that it might be possible that the symbolGraph would have
w associated with the first instance of x inside f() instead of 
the x on the left hand side. Thus, dominantSymbol dictionary is
used to maintain the proper keys if a symbol spans multiple lines of
code. This function is intended to fix that.

This function will take in symbol tuples like ('x',4,'data',0,2)
where 'x' is the 4th character and has a type of data at paren level 0 
in equation number 2. It will maintain a lookup table of dominantSymbols
that maps the symbol name 'x' to its tuple ('x',4,'data',0,2) in a dictionary
as dominantSymbols = {'x': ('x',4,'data',0,2), ...}
'''
def getDominantSymbols(dataName,proposedKey,dominantSymbols):

    dominantSymbol = ('error: unknown symbol type', 0, proposedKey[2], 0, 0)
    #if it's a type function, indicated by 'fxn' just return the proposedKey
    if ( proposedKey[2] == 'fxn'):
        dominantSymbol = proposedKey
    #the symbol type is data and it can be updated accordingly
    elif ( proposedKey[2] == 'data' ):
        if( dataName not in dominantSymbols):
            dominantSymbol = proposedKey
            dominantSymbols[dataName] = dominantSymbol
        else:
            priorEq = dominantSymbols[dataName][4]
            priorLvl = dominantSymbols[dataName][3]
            proposedEq = proposedKey[4]
            proposedLvl = proposedKey[3]
            proposedType = proposedKey[2]

            #if on LHS of current equation, indicated by proposedLvl == -1, must update
            #o.w. must be on right side of equation and can update according to priority
            if ( proposedLvl == -1 ):
                dominantSymbols[dataName] = proposedKey
                dominantSymbol = proposedKey
            elif ( priorEq <= proposedEq and priorLvl >= proposedLvl ):
                dominantSymbol = dominantSymbols[dataName]  #do not update if pre-existing
            elif ( priorEq <= proposedEq and priorLvl < proposedLvl ):
                dominantSymbol = dominantSymbols[dataName]  #provisional, may be unnecessary
            elif ( priorEq > proposedEq ):
                dominantSymbol = ('error: something is out of order', 0, 'data', 0, 0)

    return dominantSymbol, dominantSymbols

'''
New addition to build symbol graph by adding multiple lines.
It is expected that leftHandlinesOfText and rightHandLinesOfText are lists
of texts which have already been split by the '=' sign previously.

Options are 'l' for including level and 'n' for line number in the each tuple
entry of the symbol graph.
'''
def getSymbolGraphMulti(leftHandLinesOfText,rightHandLinesOfText,opts='vn'):
    # listOfArgs=[]
    symbolGraph = dict()
    dominantSymbols = dict()  # added on 12-28-2020, to establish dominance when duplicate symbols exist

    for lineNum, text in enumerate(rightHandLinesOfText):


        #symbolGraph[leftHandLinesOfText[lineNum]] = []  # populate lowest level which eventually must point to RHS
        # left names have char location of -1, type data', level -1
        leftTupleInit = (leftHandLinesOfText[lineNum],-1,'data',-1,lineNum)
        symbolGraph[leftTupleInit] = []

        symbolsByLevel = dict()
        listOfSymbols = []
        N = len(text)

        # Get paren level, indicated by number of successive "("
        # Also, get funciton level, indicated by number of "<char>(" pattern
        #listOfFxnLvl, listOfParenLvl = getParenLvl2(text)
        listOfFxnLvl, listOfParenLvl = getParenLvl3(text)

        # take difference of Function level, indicated by "<char>(" pattern
        diff_lvl = [listOfFxnLvl[k + 1] - listOfFxnLvl[k] for k in range(0, N-1)]
        #print(listOfFxnLvl)
        #print(diff_lvl)

        # Populate 0 level symbols
        k = 0
        while (k < N):
            # print(text[k],k,listOfFxnLvl[k])
            if (k <= (N - 1) and \
                    listOfFxnLvl[k] == 0 and \
                    text[k].isalnum()):
                # and not text[k+1].isalnum()
                #
                # lvl0Name, unused = getSymbolByPos(k,text)
                #
                lvl0Name, k = getSymbolLnR(k, text)  # get the symbol and move to next k
                # print(lvl0Name,k)
                # symbolGraph['###'].append((lvl0Name, k))
                # symbolGraph['###'].append((lvl0Name, k-1))  # changed 11-12-2020, see above
                #
                # New code, 12/23/2020
                # if it's a fxn, there should be a '(' to the right
                # o.w. it's a symbol that represents data.
                # if (k <= (N - 1) and text[k] == '('):
                #    symbolGraph['###']append((lvl0Name, k - 1, 'fxn'))
                # else:
                #    symbolGraph['###'].append((lvl0Name, k - 1, 'data'))
                symbolTuple = (lvl0Name,) #add in the name of the Symbol at lvl 0
                if ( k <= (N - 1) and text[k] == '('):
                    symbolTuple += (k-1,'fxn')  #include last char, k-1 and 'fxn' tag
                else:
                    symbolTuple += (k-1,'data')  #use -1 b/c instances of data are unique and 'data' tag

                if ('v' in opts):
                    symbolTuple += (0,)  #add in level number, 0 here
                if ('n' in opts):
                    symbolTuple += (lineNum,)  #add in line Number

                #New code added 12/28/2020 to incorporate dominantSymbol feature
                # if applicable, this will replace symbolTuple with the dominant symbol in dominantSymbols{}
                # it will also update the dominantSymbols{} dictionary whose keys are the symbol name.
                # The values of the dominantSymbols{} dictionary are the symbol tuples.
                symbolTuple, dominantSymbols = getDominantSymbols(lvl0Name, symbolTuple, dominantSymbols)

                symbolGraph[leftTupleInit].append(symbolTuple)  #changed key on 12/28/2020, was ###
            else:
                k += 1

        # Populate heirarchy of symbols
        for lvl in range(0, max([max(listOfFxnLvl), 1])):
            ###### find edges of lvl to lvl+1 ######
            # Initialization
            start = 0
            fin = 0
            fxnNames = []
            fxnName = None
            k = 0
            # print(lvl)
            # for k in range(0,N):
            while (k < N):
                #print(lvl, k)
                if (k < (N - 1) and \
                        listOfFxnLvl[k] == lvl and \
                        diff_lvl[k] == 1 and \
                        text[k].isalnum()):
                    # fxnName, unused = getSymbolByPos(k,text)
                    fxnName = getFxnLeft(k, text)
                    # fxnName, unused = getSymbolLnR(k,text)
                    # print(fxnName, k)
                    start = k
                    #k += 1 #new
                #elif (k == (N - 1) or \
                elif ( ( (k <= (N-2) and \
                       listOfFxnLvl[k] == (lvl+1) and \
                       diff_lvl[k] == -1) or \
                         ( k == (N-1) and \
                         listOfFxnLvl[k] == (lvl+1) )
                       ) and \
                      fxnName is not None ): # OR condition added 11-12-2020
                    fin = k
                    fxnNames.append((fxnName, start, fin))
                k += 1
                    # k += 1 #new
                #else:
                    #k += 1
            #print(fxnNames)
            ##### grab symbols at level = lvl+1 #####
            for item in fxnNames:
                tempSym = []  # clear temporary symbol list
                fName = item[0]
                start = item[1]
                fin = item[2]
                # print(fin,N,len(diff_lvl))
                k = start
                while (k <= fin):
                    if (listOfFxnLvl[k] == (lvl + 1) and \
                            text[k].isalnum()):
                        symName, k = getSymbolLnR(k, text)  # special note: advances k += 1 or more
                        if (symName is not None):
                            # tempSym.append((symName, k-1))  # changed from k to k-1, 11-12-2020
                            #
                            # New code, 12/23/2020
                            # if it's a fxn, there should be a '(' to the right
                            # o.w. it's a symbol that represents data.
                            #if (k <= (N - 1) and text[k] == '('):
                            #    tempSym.append((symName, k - 1, 'fxn'))
                            #else:
                            #    tempSym.append((symName, k - 1, 'data'))
                            #
                            # New code, 12/23/2020
                            # if it's a fxn, there should be a '(' to the right
                            # o.w. it's a symbol that represents data.
                            symbolTuple = (symName,)  # add in the name of the Symbol at lvl 0
                            if (k <= (N - 1) and text[k] == '('):
                                symbolTuple += (k - 1, 'fxn')  # include last char, k-1 and 'fxn' tag
                            else:
                                symbolTuple += (k - 1, 'data')  # use -1 b/c instances of data are unique and 'data' tag
                            if ('v' in opts):
                                symbolTuple += (lvl+1,)  # add in level number for symbol, one more than fxn
                            if ('n' in opts):
                                symbolTuple += (lineNum,)  # add in line Number

                            # New code added 12/28/2020 to incorporate dominantSymbol feature
                            # if applicable, this will replace symbolTuple with the dominant symbol in dominantSymbols{}
                            # it will also update the dominantSymbols{} dictionary whose keys are the symbol names.
                            # The values of the dominantSymbols{} dictionary are the symbol tuples.
                            symbolTuple, dominantSymbols = getDominantSymbols(symName, symbolTuple, dominantSymbols)

                            tempSym.append(symbolTuple)
                        else:
                            k += 1
                    else:
                        k += 1
                    # symbolGraph[fName] = tempSym.copy()
                    # symbolGraph[(fName,start)] = tempSym.copy()  # changed 11-12-2020, see above
                    # symbolGraph[(fName, start,'fxn')] = tempSym.copy() #New code, 12-23-2020
                    #New code below added 12-26-2020
                    tempKey=(fName,start,'fxn')
                    if ('v' in opts):
                        tempKey += (lvl,)  # add in level number, 0 here
                    if ('n' in opts):
                        tempKey += (lineNum,)  # add in line Number
                    symbolGraph[tempKey] = tempSym.copy()

        #At the end of the line of text, must add left hand side symbol to dominantSymbols
        leftName = leftHandLinesOfText[lineNum]
        leftTuple = (leftName,-1,'data',-1,lineNum)  # left names have char location of -1, type data', level -1
        unused, dominantSymbols = getDominantSymbols(leftName, leftTuple, dominantSymbols)
        #move onto the next line of text from here...

    return symbolGraph

'''
getRowMulti() returns the row assignment for the item, myKey, which must be a tuple in
the format (symbolName='someString',characterNumber=integer,type='data' or 'fxn',
lineNumber=integer)

Needed to amend getRow() for multi-line expressions to differentiate between
row values on one equation vs. the other. This is called by getRowsByKeyMulti()
'''
def getRowMulti(myKey, symbolGraph, rowsByKey, farRow):
    #case 1: no children
    if ( myKey not in symbolGraph \
        and myKey not in rowsByKey ):
        row = farRow
        farRow -= 1
    #case 2: children found, point to minimum (in absolute value sense)
    elif ( myKey in symbolGraph ):
        eqNo = myKey[4]
        #print(myKey,eqNo)
        maxList=[]  # trying to get the maximum of a negative number
        for item in symbolGraph[myKey]:
            if ( item in rowsByKey \
                and item[4] == eqNo):
                maxList.append(rowsByKey[item])
        if (len(maxList) >= 1):
            row = max(maxList)  #trying to get the maximum of a negative number
        else:
            row = farRow  # this can happen if fxn takes all args from earlier eq.
            farRow -= 1  # new line, 1-4-2020
    else:
        row = farRow
    return row, farRow

'''
The getRowsByKeyMulti() returns a lookup table, rowsByKey, as a Python dictionary 
that allows one to get the row assignment for any given symbol (key or value) in 
the symbolGraph.
'''
def getRowsByKeyMulti(symbolGraph):

    rowsByKey = {}
    leftKeys = [leftSym for leftSym in list(symbolGraph.keys()) if leftSym[3] == -1]  # new code, 12-30-2020
    row = 0  # unused, currently
    lvl = -1  # unused, currently
    farRow = 0
    #rowsByKey[myKeys[0]]=0
    for leftKey in leftKeys:
        rStack = []
        rStack.append(leftKey)  # new line, 12-31-2020
        #rowsByKey[myKey]=farRow  # new line, 12-31-2020
        # new call to rowsByKey, 12-31-2020
        rowsByKey[rStack[-1:][0]], farRow = getRowMulti(rStack[-1:][0],
                                                   symbolGraph,
                                                   rowsByKey,
                                                   farRow)
        #print(farRow, rStack[-1:][0])
        iter = 0
        stackNotEmpty = True
        myKey = leftKey  # added on 1-4-2020 to clear bug
        #farRow = 0
        while (stackNotEmpty):
            child = True
            while (child):
                k = 0
                N = len(symbolGraph[myKey])
                # print('myKey = ', myKey[0])
                while (k < N and \
                       symbolGraph[myKey][k] in rowsByKey):
                    k += 1
                while ( k < N and \
                      symbolGraph[myKey][k] not in rowsByKey ):
                    if ( symbolGraph[myKey][k] in symbolGraph ):
                        rStack.append(symbolGraph[myKey][k])
                    k += 1
                for item in symbolGraph[myKey]:
                    if (item not in symbolGraph \
                            and item not in rowsByKey):
                        child = False
                        rStack.append(item)
                if (k < N and symbolGraph[myKey][k] in symbolGraph):  # added on 1-4-2020 to clear bug
                    myKey = symbolGraph[myKey][k]
                else:
                    child = False

            childRowsWereInStack = True
            moreSymbolsFound = False
            while ( childRowsWereInStack and \
                   (not moreSymbolsFound) and \
                   len(rStack) > 0):
                #print(rStack[-1:][0], childRowsAssigned, moreSymbolsFound)
                #print(rStack[-1:][0])
                if (rStack[-1:][0] not in symbolGraph):
                    # rowsByKey[rStack[-1:][0]] = row  # assign row
                    # changed on 12-31-2020, was calling getRow(), now calls getRowMulti()
                    rowsByKey[rStack[-1:][0]], farRow = getRowMulti(rStack[-1:][0],
                                                               symbolGraph,
                                                               rowsByKey,
                                                               farRow)
                    #print(farRow, rStack[-1:][0])
                    del rStack[-1:]  # pop item
                else:
                    childRowsWereInStack = True
                    for item in symbolGraph[rStack[-1:][0]]:
                        #print(item, (item in symbolGraph))
                        if (item not in rowsByKey and \
                                item not in symbolGraph):
                            childRowsWereInStack = False
                        elif (item not in rowsByKey and \
                              item in symbolGraph):
                            moreSymbolsFound = True
                    if (childRowsWereInStack and not moreSymbolsFound):
                        # rowsByKey[rStack[-1:][0]] = row
                        # changed on 12-31-2020, was calling getRow(), now calls getRowMulti()
                        rowsByKey[rStack[-1:][0]], farRow = getRowMulti(rStack[-1:][0],
                                                                   symbolGraph,
                                                                   rowsByKey,
                                                                   farRow)
                        #print(farRow, rStack[-1:][0])
                        del rStack[-1:]  # pop item

            #print( rStack )
            if (len(rStack) > 0):
                myKey = rStack[-1:][0]
            iter += 1
            stackNotEmpty = (len(rStack) > 0 and iter <= 200)
    #myKey = '###' # old code
    #myKey = list(symbolGraph.keys())[0]  # get root of symbolGraph, cast keys to list and get 0th entry

    # print(stackNotEmpty)
    return rowsByKey
