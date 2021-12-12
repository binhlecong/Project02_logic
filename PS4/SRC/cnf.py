from const import *


def cnf(s):
    s = biCondElimination(s)
    s = impliElimination(s)
    s = demorgan(s)
    s = twoNegElimination(s)
    s = binaryize(s)
    s = distrib(s)
    # print("before andCombine:", s)
    s = andCombine(s)
    # print("before orCombine:", s)
    s = orCombine(s)
    # print("after orCombine:", s)
    s = duplicateLiteralsElination(s)
    s = duplicateClausesElimination(s)
    return s


def biCondElimination(s):
    if type(s) is str:
        return s
    elif s[0] == IFF:
        return([AND,
                [IF,
                 biCondElimination(s[1]),
                 biCondElimination(s[2])],
                [IF,
                 biCondElimination(s[2]),
                 biCondElimination(s[1])]])
    else:
        return([s[0]] + [biCondElimination(i) for i in s[1:]])


def impliElimination(s):
    if type(s) is str:
        return s
    elif s[0] == IF:
        return([OR,
                [NOT,
                 impliElimination(s[1])],
                impliElimination(s[2])])
    else:
        return([s[0]] + [impliElimination(i) for i in s[1:]])


def twoNegElimination(s):
    if type(s) is str:
        return s
    elif s[0] == NOT and type(s[1]) is list and s[1][0] == NOT:
        return(twoNegElimination(s[1][1]))
    else:
        return([s[0]] + [twoNegElimination(i) for i in s[1:]])


def demorgan(s):
    revision = demorgan1(s)
    if revision == s:
        return s
    else:
        return demorgan(revision)


def demorgan1(s):
    if type(s) is str:
        return s
    elif s[0] == NOT and type(s[1]) is list and s[1][0] == AND:
        return([OR] + [demorgan([NOT, i]) for i in s[1][1:]])
    elif s[0] == NOT and type(s[1]) is list and s[1][0] == OR:
        return([AND] + [demorgan([NOT, i]) for i in s[1][1:]])
    else:
        return ([s[0]] + [demorgan(i) for i in s[1:]])


def binaryize(s):
    if type(s) is str:
        return s
    elif s[0] == AND and len(s) > 3:
        return([AND, s[1], binaryize([AND] + s[2:])])
    elif s[0] == OR and len(s) > 3:
        return([OR, s[1], binaryize([OR] + s[2:])])
    else:
        return([s[0]] + [binaryize(i) for i in s[1:]])


def distrib(s):
    revision = distribOnBi(s)
    if revision == s:
        return s
    else:
        return distrib(revision)


def distribOnBi(s):
    if type(s) is str:
        return s
    elif s[0] == OR and type(s[1]) is list and s[1][0] == AND:
        # distribute s[2] over s[1]
        return([AND] + [distrib([OR, i, s[2]]) for i in s[1][1:]])
    elif s[0] == OR and type(s[2]) is list and s[2][0] == AND:
        # distribute s[1] over s[2]
        return([AND] + [distrib([OR, i, s[1]]) for i in s[2][1:]])
    else:
        return ([s[0]] + [distrib(i) for i in s[1:]])


def andCombine(s):
    revision = andCombine1(s)
    if revision == s:
        return s
    else:
        return andCombine(revision)


def andCombine1(s):
    if type(s) is str:
        return s
    elif s[0] == AND:
        result = [AND]
        for i in s[1:]:
            if type(i) is list and i[0] == AND:
                result = result + i[1:]
            else:
                result.append(i)
        return result
    else:
        return([s[0]] + [andCombine1(i) for i in s[1:]])


def orCombine(s):
    revision = orCombine1(s)
    if revision == s:
        return s
    else:
        return orCombine(revision)


def orCombine1(s):
    if type(s) is str:
        return s
    elif s[0] == OR:
        result = [OR]
        for i in s[1:]:
            if type(i) is list and i[0] == OR:
                result = result + i[1:]
            else:
                result.append(i)
        return result
    else:
        return([s[0]] + [orCombine1(i) for i in s[1:]])


def duplicateLiteralsElination(s):
    if type(s) is str:
        return s
    if s[0] == NOT:
        return s
    if s[0] == AND:
        return([AND] + [duplicateLiteralsElination(i) for i in s[1:]])
    if s[0] == OR:
        remains = []
        for l in s[1:]:
            if l not in remains:
                remains.append(l)
        if len(remains) == 1:
            return remains[0]
        else:
            return([OR] + remains)


def duplicateClausesElimination(s):
    if type(s) is str:
        return s
    if s[0] == NOT:
        return s
    if s[0] == OR:
        return s
    if s[0] == AND:
        remains = []
        for c in s[1:]:
            if unique(c, remains):
                remains.append(c)
        if len(remains) == 1:
            return remains[0]
        else:
            return([AND] + remains)


def unique(c, remains):
    for p in remains:
        if type(c) is str or type(p) is str:
            if c == p:
                return False
        elif len(c) == len(p):
            if len([i for i in c[1:] if i not in p[1:]]) == 0:
                return False
    return True

# def removeNeg(s):
#     if type(s) == str:
#         return s
#     elif type(s) == list and len(s) >= 2:


# if __name__ == "__main__":

#     sentences = [AND,
#                  [NOT, 'P11'],
#                  [IFF, 'B11', [OR, 'P12', 'P21']],
#                  [IFF, 'B21', [OR, 'P11', 'P22', 'P31']],
#                  [NOT, 'B11'],
#                  'B21',
#                  'P12']
#     test = [AND, 'P12', [OR, [NOT, 'P12'], 'P21']]
#     testand = [OR, 'P12', [AND, [NOT, 'P12'], 'P21']]
#     # print(orCombine(testand))
#     print(repr(cnf(sentences)))
#     print(repr(cnf(test)))
#     print(repr(cnf(testand)))
