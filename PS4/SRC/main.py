from resolution import *
from knowledge_base import *
from file_io import *
from const import *


def main():
    '''Main function'''
    start = 1
    end = 5
    for i in range(start, end + 1):
        # Read from input_.txt
        alpha, kb = read_file('input/input{}.txt'.format(str(i)))
        # Call PL-Resolution fucntion
        output, result = pl_resolution(alpha, kb)
        # Write to output_.txt
        write_file('output/output{}.txt'.format(str(i)), output, result)


if __name__ == "__main__":
    main()
