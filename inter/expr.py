from lexer.lexer import *


class Expr:
    op = None
    type_1 = None

    def __init__(self, tok, p):
        self.op = tok
        self.type_1 = p


true = Expr(TRUE, BOOL)
false = Expr(FALSE, BOOL)
