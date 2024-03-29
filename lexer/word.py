from lexer.tag import *
from lexer.token import *


class Word(Token, object):
    lexeme = ''

    def __init__(self, s, tag):
        super(Word, self).__init__(tag)
        self.lexeme = s

    def __str__(self):
        return self.lexeme


eq = Word('==', Tag.EQ)
ne = Word('!=', Tag.NE)
le = Word('<=', Tag.LE)
ge = Word('>=', Tag.GE)
minus = Word('minus', Tag.MINUS)
TRUE = Word('TRUE', Tag.TRUE)
FALSE = Word('FALSE', Tag.FALSE)
