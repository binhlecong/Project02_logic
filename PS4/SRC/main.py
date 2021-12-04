from algorithm import *
from file_io import *
from const import *


def main():
    '''Main function'''
    # Read from input.txt
    alpha = 'A'
    problem = [AND,
               'A',
               [OR, 'B', 'C', [NOT, 'B'], [NOT, 'C']],
               [OR, 'X', 'Y', 'Z'],
               [NOT, 'A'],
               ]

    alpha = [OR, 'B', [NOT, 'B']]
    problem = [AND,
               'A',
               [OR, 'B', 'C', [NOT, 'B'], [NOT, 'C']],
               [OR, 'X', 'Y', 'Z'],
               [NOT, 'A'],
               ]

    kb = KnowledgeBase()
    kb.detailsTurn = True
    for cl in problem[1:]:
        kb.tell(cl)

    # Call PL-Resolution fucntion
    output, result = plResolution(kb, alpha)

    # Write to output.txt
    for loop in output:
        print(len(loop))
        for clause in loop:
            print(clause)
    print(result)


if __name__ == "__main__":
    main()
