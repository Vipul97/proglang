from lexer.Lexer import *


class Expr:
    op = None
    type1 = None

    def __init__(self, tok, p):
        self.op = tok
        self.type1 = p

true = Expr(TRUE, BOOL)
false = Expr(FALSE, BOOL)
