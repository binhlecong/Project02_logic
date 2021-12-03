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

    # Call PL-Resolution
    print(plResolution(kb, alpha))

    # Write to output.txt


if __name__ == "__main__":
    main()
