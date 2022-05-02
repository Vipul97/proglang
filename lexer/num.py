from lexer.token import *
from lexer.tag import *


class Num(Token, object):
    value = None

    def __init__(self, v):
        super(Num, self).__init__(Tag.NUM)
        self.value = v
