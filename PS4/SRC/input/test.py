import random

kb = []

test_from = 3
test_to = 3

'''gen CFN sz literal into file F'''
def gen_clause(sz, f):
    while True:
        res = []
        for i in range(sz):
            while True:
                c = random.randint(0, 6)
                c = chr(ord('A') + c)
                sign = random.randint(0, 1)
                if sign == 1: c = '-' + c
                if c not in res:
                    res.append(c)
                    break
        res = sorted(res, key = lambda x: (x if len(x) == 1 else x[1]))
        if res not in kb:
            break
    f.write(' OR '.join(res) + '\n')

def gen_test():
    # return
    for id in range(test_from, test_to + 1):
        kb.clear
        n = random.randint(6, 8) # number of clauses
        f = open("./input" + str(id) + ".txt", "w")
        gen_clause(random.randint(2, 3), f)
        f.write(str(n) + '\n')
        for i in range(n):
            gen_clause(random.randint(1, 3), f)
        f.close()
        
gen_test()