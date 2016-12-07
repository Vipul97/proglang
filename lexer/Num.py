from lexer.Token import *
from lexer.Tag import *


class Num(Token, object):
    value = None

    def __init__(self, v):
        super(Num, self).__init__(Tag.NUM)
        self.value = v
