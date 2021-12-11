from algorithm import *
from file_io import *
from const import *


def main():
    '''Main function'''
    for i in range(1, 6):
        # Read from input_.txt
        alpha, kb = read_file('input/input{}.txt'.format(str(i)))
        # Call PL-Resolution fucntion
        output, result = plResolution(kb, alpha)
        # Write to output_.txt
        write_file('output/output{}.txt'.format(str(i)), output, result)


if __name__ == "__main__":
    main()
