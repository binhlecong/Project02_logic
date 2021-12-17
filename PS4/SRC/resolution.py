from my_utils import sortClause
import cnf
from const import *


def pl_resolution(alpha, kb):
    '''Main algorithm to solve problem'''
    clauses = kb.clauses + discombine(AND, cnf.cnf(negative_inside(alpha)))
    newList = []
    output = []
    while True:
        # subSumption(clauses)
        n = len(clauses)
        pairs = [(clauses[i], clauses[j])
                 for i in range(n) for j in range(i+1, n)]
        tmpList = []
        for (ci, cj) in pairs:
            if is_resolvable(ci, cj):
                resolvents = pl_resolve(ci, cj)
                for tempCR in resolvents:
                    if not tempCR in clauses and not tempCR in newList:
                        newList.append(tempCR)
                        tmpList.append(tempCR)
        # Add clauses of this loop to the output
        output.append(tmpList)
        # Remove tautology
        newList = [item for item in newList if not has_tautology(item)]
        # Return result
        if is_sublist_of(newList, clauses):
            return output, False
        # Insert generated clauses into clauses
        for item in newList:
            if not item in clauses:
                clauses.append(item)
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


def discombine(op, clause):
    '''Return the discombination(list) of clause'''
    if type(clause) == str:
        return [clause]
    elif len(clause) <= 2:
        return [clause]
    elif op == clause[0]:
        return clause[1:]
    else:
        return [clause]


def has_tautology(clause):
    '''Return excess clause like ['P', [NOT, 'P']]'''
    if type(clause) == str or len(clause) <= 1:
        return False
    else:
        for item in clause:
            if negative_inside(item) in clause:
                return True
    return False


def is_resolvable(ci, cj):
    '''Check if 2 clauses are worth resolving according to the assignment'''
    cnt = 0
    for di in discombine(OR, ci):
        for dj in discombine(OR, cj):
            if di == negative_inside(dj) or negative_inside(di) == dj:
                cnt += 1
    return cnt == 1


def pl_resolve(cl_i, cl_j):
    '''Resolve the two clauses'''
    clauses = []
    for di in discombine(OR, cl_i):
        for dj in discombine(OR, cl_j):
            if di == negative_inside(dj) or negative_inside(di) == dj:
                diNew = discombine(OR, cl_i)
                diNew.remove(di)
                djNew = discombine(OR, cl_j)
                djNew.remove(dj)
                dNew = diNew + djNew
                dNew = to_unique(dNew)
                toAddD = combine(OR, dNew)
                # Keep the literals in alphabetical order
                sortClause(toAddD)
                # Add the clauses to the result
                clauses.append(toAddD)
    return clauses


def negative_inside(cl):
    '''Move negation sign inside cl'''
    if type(cl) == str:
        return [NOT, cl]
    elif cl[0] == NOT:
        return cl[1]
    elif cl[0] == AND:
        tempRet = [OR]
        for element in cl[1:]:
            tempRet.append(negative_inside(element))
        return tempRet
    elif cl[0] == OR:
        tempRet = [AND]
        for element in cl[1:]:
            tempRet.append(negative_inside(element))
        return tempRet


def to_unique(clauses):
    '''Return a list of clauses in which items are unique'''
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


def is_sublist_of(l_i, l_j):
    '''Check if l1 is sublist of l2'''
    for element in l_i:
        if not element in l_j:
            return False
    return True
