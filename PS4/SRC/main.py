import cnf

def toUnique(clauses):
    '''
    return a clauses list whose elements are unique
    '''
    if type(clauses) == str:
        return clauses
    if len(clauses) == 0:
        return clauses
    retClauses = []

    strElementList = list(set([str(element) for element in clauses]))

    for element2 in strElementList:
        if '[' in element2:
            retClauses.append(eval(element2))
        else:
            retClauses.append(element2)
    return retClauses


def combine(op, elements):
    '''
    return the combination of elements using operation op
    '''
    if len(elements) == 0:
        return elements
    elif len(elements) == 1:
        return elements[0]
    elif op == 'and':
        return ['and'] + elements
    elif op == 'or':
        return ['or'] + elements


def plResolve(ci, cj):
    '''
    returns all clauses that can be obtained from clauses ci and cj
    '''
    clauses = []
    for di in disCombine('or', ci):
        for dj in disCombine('or', cj):
            if di == negativeInside(dj) or negativeInside(di) == dj:
                # global gloVar
                # if gloVar % 10 == 0:
                #     print("times: ", gloVar)
                #     print("ci is %s, and cj is %s" % (ci, cj))
                # gloVar += 1
                diNew = disCombine('or', ci)
                diNew.remove(di)
                djNew = disCombine('or', cj)
                djNew.remove(dj)
                # print("diNew:", diNew)
                # print("djNew:", djNew)
                dNew = diNew + djNew
                dNew = toUnique(dNew)
                # print("dNew:", dNew)
                toAddD = combine('or', dNew)
                # print("toAddD:", toAddD)
                clauses.append(toAddD)
    return clauses


def disCombine(op, clause):
    '''
    return the discombination(list) of clause using operation op
    '''
    result = []
    if type(clause) == str:
        return [clause]
    elif len(clause) <= 2:    # P or not P, just return self
        return [clause]
    elif op == clause[0]:
        return clause[1:]
    else:
        return [clause]


def isSublistOf(l1, l2):
    '''
    return if l1 is sublist of l2
    '''
    for element in l1:
        if not element in l2:
            return False
    return True


def orContainTautology(clause):
    '''
    return if the or clause contain the tautology
    eg: ['P', ['not', 'P']]
    '''
    if type(clause) == str or len(clause) <= 1:
        return False
    else:
        for item in clause:
            if negativeInside(item) in clause:
                return True
    return False


def negativeInside(s):
    '''
    move negation sign inside s
    '''
    if type(s) == str:
        return ['not', s]
    elif s[0] == 'not':
        return s[1]
    elif s[0] == 'and':
        tempRet = ['or']
        for element in s[1:]:
            tempRet.append(negativeInside(element))
        return tempRet
    elif s[0] == 'or':
        tempRet = ['and']
        for element in s[1:]:
            tempRet.append(negativeInside(element))
        return tempRet


def pl_resolution(kb, alpha):
    '''
    returns if KB entailments alpha True or False using pl resolution
    kb: KnowledgeBase
    alpha: the result to prove
    '''
    clauses = kb.clauses + disCombine('and', cnf.cnf(negativeInside(alpha)))
    # clauses = duplicateOrElemination(clauses)
    # if str(clauses) == list and len(clauses) == 0:
    #     return True
    newList = []
    while True:

        # subSumption(clauses)
        n = len(clauses)
        pairs = [(clauses[i], clauses[j])
                 for i in range(n) for j in range(i+1, n)]
        for (ci, cj) in pairs:
            resolvents = plResolve(ci, cj)
            if kb.detailsTurn:
                print("After doing resolution for %s and %s we get %s" %
                      (ci, cj, resolvents))
            if [] in resolvents:
                return True
            for tempCR in resolvents:
                if not tempCR in newList:
                    newList.append(tempCR)
            # newList = toUnique(newList + resolvents)
        #     print("newList:", newList)
        # print("clauses:", clauses)
        newList = [cc for cc in newList if not orContainTautology(cc)]
        # subSumption(newList)
        if isSublistOf(newList, clauses):
            return False
        for cc in newList:
            if not cc in clauses:
                clauses.append(cc)
        # clauses = toUnique(clauses + newList)
    pass


if __name__ == "__main__":
    # Read from input.txt

    # Call PL-Resolution

    # Write to output.txt
    pass
