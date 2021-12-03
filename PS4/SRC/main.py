from algorithm import *
from file_io import *
from const import *


def main():
    '''Main function'''
    # Read from input.txt
    problem = [AND,
               [OR, [NOT, 'A'], 'B'],
               [OR, 'B', [NOT, 'C']],
               [OR, 'A', [NOT, 'B'], 'C'],
               [NOT, 'B'],
               ]

    kb = KnowledgeBase()
    kb.detailsTurn = True
    for cl in problem[1:]:
        kb.tell(cl)
    alpha = 'A'

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
