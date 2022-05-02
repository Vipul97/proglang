from lexer.word import *


class Type(Word):
    def __init__(self, s, tag):
        super(Type, self).__init__(s, tag)

    def numeric(self, p):
        if p in [CHAR, NUM, REAL]:
            return True

        return False

    def max(self, p1, p2):
        if not self.numeric(p1) or not self.numeric(p2):
            return None
        elif p1 == REAL or p2 == REAL:
            return REAL
        elif p1 == NUM or p2 == NUM:
            return NUM
        else:
            return CHAR


NUM = Type('NUM', Tag.BASIC)
REAL = Type('REAL', Tag.BASIC)
CHAR = Type('CHAR', Tag.BASIC)
BOOL = Type('BOOL', Tag.BASIC)
