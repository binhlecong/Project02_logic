import os
from algorithm import KnowledgeBase
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
    for i in range(kb_size):
        kb.append(str_to_struct(file.readline()))
    # Close file
    file.close()
    # Create a KnowledgeBase from list
    knowledgeBase = KnowledgeBase()
    knowledgeBase.detailsTurn = True
    for cl in kb[1:]:
        knowledgeBase.tell(cl)
    return alpha, knowledgeBase


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
