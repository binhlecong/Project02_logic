from const import AND
import cnf
from resolution import discombine


class KnowledgeBase:
    '''KnowledgeBase class'''

    def __init__(self, sentence=None):
        self.clauses = []
        if sentence:
            self.add(sentence)

    def add(self, sentence):
        self.clauses.extend(discombine(AND, cnf.cnf(sentence)))
