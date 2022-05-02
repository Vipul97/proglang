from symbols.type import *


class Array(Type):
    of = None

    def __init__(self, p):
        super(Array, self).__init__("[]", Tag.INDEX)
        self.of = p
