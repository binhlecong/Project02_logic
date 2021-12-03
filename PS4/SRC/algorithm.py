import random
import cnf
from const import *


class KnowledgeBase:
    '''
    A KnowledgeBase for Propositional logic.
    '''

    def __init__(self, sentence=None):
        self.clauses = []
        self.detailsTurn = False    # print the algorithm details or not
        if sentence:
            self.tell(sentence)

    def tell(self, sentence):
        '''
        Add the sentence to KnowledgeBase
        also reduce it to smallest structure
        '''
        self.clauses.extend(disCombine(AND, cnf.cnf(sentence)))

# ______________________________________________________________________________
# Truth table enumeration method


def combine(op, elements):
    '''
    return the combination of elements using operation op
    '''
    if len(elements) == 0:
        return elements
    elif len(elements) == 1:
        return elements[0]
    elif op == AND:
        return [AND] + elements
    elif op == OR:
        return [OR] + elements


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


def tTEntails(kb, alpha):
    '''
    returns if KB entailments alpha True or False using truth table
    kb: KnowledgeBase
    alpha: the result to prove
    '''
    clauses = kb.clauses + disCombine(AND, cnf.cnf(alpha))
    symbols = propSymbols(combine(AND, clauses))

    return tTCheckAll(kb, alpha, symbols, {})


call_times = 0


def tTCheckAll(kb, alpha, symbols, model):
    '''
    help to implement tTEntails
    model is a dictionary such as {'P': True, "Q": False}
    '''

    if len(symbols) == 0:
        alphaCnf = cnf.cnf(alpha)
        # print("kb:", kb.clauses)
        if kb.detailsTurn:
            print("model:", model)
            print("result:", plTrue(alphaCnf, model))
        # print("\n")
        # global call_times
        # print("call_times:", call_times)
        # call_times+=1
        if plTrue(cnf.cnf(combine(AND, kb.clauses)), model):
            return plTrue(alphaCnf, model)
        else:
            return True     # when KB is false, always return True
    else:
        p, rest = symbols[0], symbols[1:]
        return (tTCheckAll(kb, alpha, rest, modelExtend(model, p, True)) and tTCheckAll(kb, alpha, rest, modelExtend(model, p, False)))


def plTrue(clause, model={}):
    '''
    Return True if the clause is true in the model, and False if it is false.
    Return None if the model does not specify all symbols
    '''
    assert len(model) > 0, 'the length of model should be more than 0'
    assert len(clause) > 0, 'the length of clause should be more than 0'
    if type(clause) == str:
        return model[clause]
    elif len(clause) >= 2:   # must be the type of list
        if clause[0] == NOT:
            return not plTrue(clause[1], model)
        elif clause[0] == AND:
            clauseRest = combine(AND, clause[2:])
            if len(clauseRest) == 0:    # if operation is AND, remove the influence of []
                return plTrue(clause[1], model)
            else:
                return plTrue(clause[1], model) and plTrue(clauseRest, model)
        elif clause[0] == OR:
            clauseRest = combine(OR, clause[2:])
            if len(clauseRest) == 0:
                return plTrue(clause[1], model)
            else:
                return plTrue(clause[1], model) or plTrue(clauseRest, model)


def propSymbols(clause):
    '''
    Return the list of all propositional symbols in cnfClause.
    '''
    if len(clause) == 0:
        return []
    elif type(clause) == str:
        return [clause]
    elif len(clause) <= 2:   # P or not P, just return self
        return [clause[-1]]
    else:
        rtSymbols = []
        for s in clause[1:]:
            pI = propSymbols(s)
            rtSymbols.extend(list(set(pI)))
        return list(set(rtSymbols))

# ______________________________________________________________________________
# PL resolution method


def modelExtend(model, p, v):
    '''
    Return the new model with p values v added
    '''
    model2 = model.copy()
    model2[p] = v
    return model2


def duplicateOrElemination(clauses):
    '''
    Eleminate the duplicate item in or clause
    eg: [OR, 'P', [NOT, 'P']] return []
    '''
    if type(clauses) == str or len(clauses) <= 1:
        return clauses
    else:
        for item in clauses:
            if negativeInside(item) in clauses:
                return []
    return clauses


def orContainTautology(clause):
    '''
    return if the or clause contain the tautology
    eg: ['P', [NOT, 'P']]
    '''
    if type(clause) == str or len(clause) <= 1:
        return False
    else:
        for item in clause:
            if negativeInside(item) in clause:
                return True
    return False


def subSumption(clauses):
    '''
    return if the or clause contain the tautology
    eg: ['P', [AND, 'P', "Q"]] return ['P']
    '''
    unitClauses = [item for item in clauses if type(
        item) == str or (type(item) == list) and len(item) == 2]
    print("unitClauses:", unitClauses)
    print("before sub:", clauses)
    for cc in clauses:
        for unitC in unitClauses:
            if type(cc) == list and len(cc) > 2:
                if unitC in disCombine(OR, cc) and cc in clauses:
                    clauses.remove(cc)
    print("After sub:", clauses)


def plResolution(kb, alpha):
    '''
    returns if KB entailments alpha True or False using pl resolution
    kb: KnowledgeBase
    alpha: the result to prove
    '''
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


def isResolvable(ci, cj):
    '''
    Check if 2 clauses are worth resolving according to the assignment 
    '''
    cnt = 0
    for di in disCombine(OR, ci):
        for dj in disCombine(OR, cj):
            if di == negativeInside(dj) or negativeInside(di) == dj:
                cnt += 1
    return cnt == 1


def plResolve(ci, cj):
    '''
    Returns all clauses that can be obtained from clauses ci and cj
    '''
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


def sortClause(clause):
    '''
    Return clause in alphabetical order
    '''
    for i in range(1, len(clause)):
        # Turn flag off
        swapped = False
        # loop to compare array elements
        for j in range(1, len(clause) - i):
            # compare two adjacent elements
            # change > to < to sort in descending order
            valueOfJ = clause[j] if isinstance(
                clause[j], str) else clause[j][1]
            valueOfJ_1 = clause[j + 1] if isinstance(
                clause[j + 1], str) else clause[j + 1][1]

            #print(valueOfJ, valueOfJ_1)
            if valueOfJ > valueOfJ_1:
                # Swap elements
                temp = clause[j]
                clause[j] = clause[j + 1]
                clause[j + 1] = temp
                # Turn flag on
                swapped = True
        # Stop algorithm when there were no sort
        if not swapped:
            break


def negativeInside(s):
    '''
    move negation sign inside s
    '''
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


def isSublistOf(l1, l2):
    '''
    return if l1 is sublist of l2
    '''
    for element in l1:
        if not element in l2:
            return False
    return True


# ______________________________________________________________________________
# WaklSAT method


def walkSAT(clauses, p=0.5, maxFlips=10000):
    '''
    returns every symbols' result by randomly flipping values of variables for maxFlips times and check its satisfiability
    clauses: the clauses to check
    p: the probability of flipping the value of the symbol
    maxFlip: maximum flipping time
    '''
    symbols = propSymbols(combine(AND, clauses))
    print("symbols: ", symbols)

    model = {s: random.choice([True, False]) for s in symbols}
    for i in range(maxFlips):
        print("running time:", i)
        satisfied, unsatisfied = [], []
        for clause in clauses:
            if plTrue(clause, model):
                satisfied.append(clause)
            else:
                unsatisfied.append(clause)
        if len(unsatisfied) == 0:  # if model satisfied all the clauses
            return model
        clause = random.choice(unsatisfied)
        if p > random.uniform(0.0, 1.0):
            sym = random.choice(list(propSymbols(clause)))
        else:
            def sat_count(sym):
                # Return the number of clauses satisfied after flipping the symbol.
                model[sym] = not model[sym]
                count = len(
                    [clause for clause in clauses if plTrue(clause, model)])
                model[sym] = not model[sym]
                return count
            sym = max(propSymbols(clause), key=sat_count)
        model[sym] = not model[sym]
    # Return None if no solution is found within the flip limit
    return None


if __name__ == "__main__":
    ''' Testing '''

    problem1 = [AND,
                [OR, [NOT, 'A'], 'B'],
                [OR, [NOT, 'C'], 'B'],
                [OR, 'A', [NOT, 'B'], 'C'],
                [NOT, 'B'],
                ]
    alpha = [NOT, 'A']
    # alpha = 'A'

    kb = KnowledgeBase()
    kb.detailsTurn = True
    for cl in problem1[1:]:
        kb.tell(cl)

    print(plResolution(kb, alpha))
    print(tTEntails(kb, alpha))
