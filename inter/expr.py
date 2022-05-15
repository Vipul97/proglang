from lexer.lexer import *


class Expr:
    op = None
    type_ = None

    def __init__(self, tok, p):
        self.op = tok
        self.type_ = p


true = Expr(TRUE, BOOL)
false = Expr(FALSE, BOOL)
