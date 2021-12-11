import os
from typing import Literal
from my_utils import *
from const import AND, NOT, OR


def read_file(filepath):
    # Open file
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, filepath)
    file = open(file=path, mode='r')
    # Read alpha
    alpha = str_to_struct(file.readline())
    kb_size = int(file.readline(), base=10)
    # Read knowledgebase
    kb = [AND]
    for line in file:
        kb.append(str_to_struct(line))
    # Close file
    file.close()
    return alpha, kb


def str_to_struct(str):
    if len(str.split(OR)) == 1:
        if '-' in str:
            return [NOT, str.replace('-', '').replace(' ', '').replace('\n', '')]
        else:
            return str.replace(' ', '').replace('\n', '')
    # EXtract literal from input
    literals = str.split(OR)
    for index in range(len(literals)):
        if '-' in literals[index]:
            literals[index] = [NOT, literals[index].replace(
                ' ', '').replace('\n', '').replace('-', '')]
        else:
            literals[index] = literals[index].replace(
                ' ', '').replace('\n', '')
    # Sort literal before return
    ans = [OR]
    for literal in literals:
        ans.append(literal)
    return ans


def struct_to_str(line):
    ans = ''
    if isinstance(line, list):
        if len(line) > 0:
            if line[0] == OR:
                for literal in line[1:]:
                    ans += literal_to_str(literal)
                    ans += ' '
                    ans += OR
                    ans += ' '
                ans = ans[:-4]
                return ans
            else:
                literal_to_str(line)
        else:
            return '{}'
    return literal_to_str(line)


def literal_to_str(literal):
    if isinstance(literal, str):
        return literal
    return '-' + literal[1]


def write_file(filepath, output, result):
    # Open file
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, filepath)
    file = open(file=path, mode="w+")
    # Write into file
    for loop in output:
        file.write(str(len(loop)) + '\n')
        for clause in loop:
            file.write(struct_to_str(clause) + '\n')
    file.write(('YES' if result else 'NO') + '\n')
    # Close file
    file.close()
