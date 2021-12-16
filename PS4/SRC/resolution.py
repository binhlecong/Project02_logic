from my_utils import sortClause
import cnf
from const import *


def plResolution(kb, alpha):
    '''Main algorithm to solve problem'''
    clauses = kb.clauses + disCombine(AND, cnf.cnf(negativeInside(alpha)))
    newList = []
    output = []
    while True:
        # subSumption(clauses)
        n = len(clauses)
        pairs = [(clauses[i], clauses[j])
                 for i in range(n) for j in range(i+1, n)]
        tmpList = []
        for (ci, cj) in pairs:
            if isResolvable(ci, cj):
                resolvents = plResolve(ci, cj)
                #
                for tempCR in resolvents:
                    if not tempCR in clauses and not tempCR in newList:
                        newList.append(tempCR)
                        tmpList.append(tempCR)
        # Add clauses of this loop to the output
        output.append(tmpList)
        # Remove tautology
        newList = [cc for cc in newList if not orContainTautology(cc)]
        # Return result
        if isSublistOf(newList, clauses):
            return output, False
        # Insert generated clauses into clauses
        for cc in newList:
            if not cc in clauses:
                clauses.append(cc)
        # Return result
        if [] in clauses:
            return output, True


def combine(op, elements):
    '''Return the combination of elements'''
    if len(elements) == 0:
        return elements
    elif len(elements) == 1:
        return elements[0]
    elif op == AND:
        return [AND] + elements
    elif op == OR:
        return [OR] + elements


def disCombine(op, clause):
    '''Return the discombination(list) of clause'''
    if type(clause) == str:
        return [clause]
    elif len(clause) <= 2:
        return [clause]
    elif op == clause[0]:
        return clause[1:]
    else:
        return [clause]


def orContainTautology(clause):
    '''Return excess clause like ['P', [NOT, 'P']]'''
    if type(clause) == str or len(clause) <= 1:
        return False
    else:
        for item in clause:
            if negativeInside(item) in clause:
                return True
    return False


def isResolvable(ci, cj):
    '''Check if 2 clauses are worth resolving according to the assignment '''
    cnt = 0
    for di in disCombine(OR, ci):
        for dj in disCombine(OR, cj):
            if di == negativeInside(dj) or negativeInside(di) == dj:
                cnt += 1
    return cnt == 1


def plResolve(ci, cj):
    '''Returns all clauses that c'''
    clauses = []
    for di in disCombine(OR, ci):
        for dj in disCombine(OR, cj):
            if di == negativeInside(dj) or negativeInside(di) == dj:
                diNew = disCombine(OR, ci)
                diNew.remove(di)
                djNew = disCombine(OR, cj)
                djNew.remove(dj)
                dNew = diNew + djNew
                dNew = toUnique(dNew)
                toAddD = combine(OR, dNew)
                # Keep the literals in alphabetical order
                sortClause(toAddD)
                # Add the clauses to the result
                clauses.append(toAddD)
    return clauses


def negativeInside(s):
    '''Move negation sign inside s'''
    if type(s) == str:
        return [NOT, s]
    elif s[0] == NOT:
        return s[1]
    elif s[0] == AND:
        tempRet = [OR]
        for element in s[1:]:
            tempRet.append(negativeInside(element))
        return tempRet
    elif s[0] == OR:
        tempRet = [AND]
        for element in s[1:]:
            tempRet.append(negativeInside(element))
        return tempRet


def toUnique(clauses):
    '''Return a clauses list whose elements are unique'''
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


def isSublistOf(l1, l2):
    '''Check if l1 is sublist of l2'''
    for element in l1:
        if not element in l2:
            return False
    return True


# if __name__ == "__main__":
#     ''' Testing '''

#     problem1 = [AND,
#                 [OR, [NOT, 'A'], 'B'],
#                 [OR, [NOT, 'C'], 'B'],
#                 [OR, 'A', [NOT, 'B'], 'C'],
#                 [NOT, 'B'],
#                 ]
#     alpha = [NOT, 'A']
#     # alpha = 'A'

#     kb = KnowledgeBase()
#     kb.detailsTurn = True
#     for cl in problem1[1:]:
#         kb.tell(cl)

#     print(plResolution(kb, alpha))
