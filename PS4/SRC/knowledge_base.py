from const import AND
import cnf
from resolution import dis_combine


class KnowledgeBase:
    '''KnowledgeBase class'''

    def __init__(self, sentence=None):
        self.clauses = []
        self.detailsTurn = False    # print the algorithm details or not
        if sentence:
            self.add(sentence)

    def add(self, sentence):
        self.clauses.extend(dis_combine(AND, cnf.cnf(sentence)))
