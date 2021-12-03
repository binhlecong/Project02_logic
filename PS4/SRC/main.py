from algorithm import *
from file_io import *


def main():
    '''Main function'''
    # Read from input.txt
    problem = ['and',
               ['or', ['not', 'A'], 'B'],
               ['or', 'B', ['not', 'C']],
               ['or', 'A', ['not', 'B'], 'C'],
               ['not', 'B'],
               ]

    kb = KnowledgeBase()
    kb.detailsTurn = True
    for cl in problem[1:]:
        kb.tell(cl)
    alpha = ['not', 'A']
    alpha='A'
    # Call PL-Resolution
    res, output = plResolution(kb, alpha)

    # Write to output.txt
    for loop in output:
        print(len(loop))
        for clause in loop:
            print(clause)
    print(res)


if __name__ == "__main__":
    main()
