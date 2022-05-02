from lexer.token import *
from lexer.tag import *


class Real(Token, object):
    value = None

    def __init__(self, v):
        super(Real, self).__init__(Tag.REAL)
        self.value = v
