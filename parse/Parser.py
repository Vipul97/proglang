from symbols.Array import *
from symbols.Env import *
from symbols.Type import *
from inter.Expr import *


class Parser:
    __lex = None
    __look = None
    top = None
    Enclosing = False

    def __init__(self, l):
        self.__lex = l
        self.move()

    def move(self):
        self.__look = self.__lex.scan()

    def error(self, s):
        print "\nnear line " + str(self.__lex.line) + ": " + s
        exit()

    def match(self, t):
        if self.__look.tag == t:
            self.move()
        else:
            self.error("syntax error, expected '" + str(t) + "', got '" + str(self.__look.lexeme) + "'")

    def Setcheck(self, p1, p2):
        if Type.numeric(p1, p1) and Type.numeric(p2, p2):
            return p2
        elif p1 == BOOL and p2 == BOOL:
            return p2
        else:
            return None

    def SetElemcheck(self, p1, p2):
        if isinstance(p1, Array) or isinstance(p2, Array):
            return None
        elif p1 == p2:
            return p2
        elif Type.numeric(p1, p1) and Type.numeric(p2, p2):
            return p2
        else:
            return None

    def program(self):
        if self.__look.tag == Tag.DEFINE:
            self.func()

    def func(self):
        self.match(Tag.DEFINE)
        self.match(Tag.BASIC)
        self.match(Tag.ID)
        self.match('(')
        savedEnv = self.top
        self.top = Env(self.top)
        self.decls()
        self.match(')')
        self.block()
        self.top = savedEnv
        self.program()

    def block(self):
        self.match(Tag.BEGIN)
        savedEnv = self.top
        self.top = Env(self.top)
        self.decls()
        self.stmts()
        self.match(Tag.END)
        self.top = savedEnv
        self.program()

    def decls(self):
        while self.__look.tag == Tag.BASIC:
            p = self.type1()
            tok = self.__look
            self.match(Tag.ID)
            self.match(';')
            id1 = Expr(tok, p)
            self.top.put(tok, id1)

    def type1(self):
        p = self.__look
        self.match(Tag.BASIC)

        if self.__look.tag != '[':
            return p
        else:
            return self.dims(p)

    def dims(self, p):
        self.match('[')
        self.match(Tag.NUM)
        self.match(']')

        if self.__look.tag == '[':
            p = self.dims(p)

        return Array(p)

    def stmts(self):
        if self.__look.tag != Tag.END:
            self.stmt()
            self.stmts()

    def stmt(self):
        if self.__look.tag == ';':
            self.move()

        elif self.__look.tag == Tag.BASIC:
            self.decls()

        elif self.__look.tag == Tag.IF:
            self.match(Tag.IF)
            self.match('(')
            x = self.bool1()
            self.match(')')
            self.stmt()

            if x.type1 != BOOL:
                self.error("boolean required in if")

            if self.__look.tag == Tag.ELSE:
                self.match(Tag.ELSE)
                self.stmt()

        elif self.__look.tag == Tag.WHILE:
            savedStmt = self.Enclosing
            self.Enclosing = True
            self.match(Tag.WHILE)
            self.match('(')
            x = self.bool1()
            self.match(')')
            self.stmt()

            if x.type1 != BOOL:
                self.error("boolean required in while")

            self.Enclosing = savedStmt

        elif self.__look.tag == Tag.DO:
            savedStmt = self.Enclosing
            self.match(Tag.DO)
            self.stmt()
            self.match(Tag.WHILE)
            self.match('(')
            x = self.bool1()
            self.match(')')
            self.match(';')

            if x.type1 != BOOL:
                self.error("boolean required in do")

            self.Enclosing = savedStmt

        elif self.__look.tag == Tag.BREAK:
            self.match(Tag.BREAK)
            self.match(';')

            if not self.Enclosing:
                self.error("unenclosed break")

        elif self.__look.tag == Tag.PRINT:
            self.match(Tag.PRINT)
            t = self.__look

            if t.tag == Tag.ID:
                self.match(Tag.ID)
                id1 = self.top.get(t)

                if not id1:
                    self.error(t.toString() + " undeclared")

            self.match(';')

        elif self.__look.tag == Tag.READ:
            self.match(Tag.READ)
            t = self.__look
            self.match(Tag.ID)
            id1 = self.top.get(t)

            if not id1:
                self.error(t.toString() + " undeclared")

            self.match(';')

        elif self.__look.tag == Tag.BEGIN:
            self.block()

        elif self.__look.tag == Tag.RETURN:
            self.match(Tag.RETURN)
            self.bool1()
            self.match(';')

        else:
            self.assign()

    def assign(self):
        t = self.__look
        self.match(Tag.ID)
        id1 = self.top.get(t)

        if not id1:
            self.move()

            if self.__look.tag == Tag.NUM:
                id1 = Expr(t, NUM)
            elif self.__look.tag == Tag.REAL:
                id1 = Expr(t, REAL)
            elif self.__look.tag == CHAR:
                id1 = Expr(t, CHAR)
            elif self.__look.tag == Tag.TRUE or self.__look.tag == Tag.FALSE:
                id1 = Expr(t, BOOL)

            self.top.put(t, id1)
            y = self.bool1()

            if not self.Setcheck(id1.type1, y.type1):
                self.error("type error")

            self.match(';')

        elif self.__look.tag == '=':
            self.move()
            y = self.bool1()

            if not self.Setcheck(id1.type1, y.type1):
                self.error("type error")

            self.match(';')

        else:
            x = self.offset(id1)
            self.match('=')
            y = self.bool1()

            if not self.SetElemcheck(x.type1, y.type1):
                self.error("type error")

            self.match(';')

    def bool1(self):
        x = self.join()

        while self.__look.tag == Tag.OR:
            tok = self.__look
            self.move()
            self.join()
            x = Expr(tok, BOOL)

        return x

    def join(self):
        x = self.equality()

        while self.__look.tag == Tag.AND:
            tok = self.__look
            self.move()
            self.equality()
            x = Expr(tok, BOOL)

        return x

    def equality(self):
        x = self.rel()

        while self.__look.tag == Tag.EQ or self.__look.tag == Tag.NE:
            tok = self.__look
            self.move()
            self.rel()
            return Expr(tok, BOOL)

        return x

    def rel(self):
        x = self.expr()

        if self.__look.tag == '<' or self.__look.tag == Tag.LE or self.__look.tag == Tag.GE or self.__look.tag == '>':
            tok = self.__look
            self.move()
            y = self.expr()
            type1 = Type.max(x.type1, x.type1, y.type1)

            if not type1:
                self.error("type error")

            return Expr(tok, BOOL)

        else:
            return x

    def expr(self):
        x = self.term()

        while self.__look.tag == '+' or self.__look.tag == '-':
            self.move()
            y = self.term()
            type1 = Type.max(x.type1, x.type1, y.type1)

            if not type1:
                self.error("type error")

        return x

    def term(self):
        x = self.unary()

        while self.__look.tag == '*' or self.__look.tag == '/':
            self.move()
            y = self.unary()
            type1 = Type.max(x.type1, x.type1, y.type1)

            if not type1:
                self.error("type error")

        return x

    def unary(self):
        if self.__look.tag == '-':
            self.move()
            x = self.unary()
            type1 = Type.max(x.type1, NUM, x.type1)

            if not type1:
                self.error("type error")

        elif self.__look.tag == Tag.NOT:
            tok = self.__look
            self.move()
            self.unary()
            return Expr(tok, BOOL)

        else:
            return self.factor()

    def factor(self):
        x = None

        if self.__look.tag == '(':
            self.move()
            x = self.bool1()
            self.match(')')
            return x

        elif self.__look.tag == Tag.NUM:
            x = Expr(Num(self.__look), NUM)
            self.move()
            return x

        elif self.__look.tag == Tag.REAL:
            x = Expr(Num(self.__look), REAL)
            self.move()
            return x

        elif self.__look.tag == Tag.TRUE:
            x = true
            self.move()
            return x

        elif self.__look.tag == Tag.FALSE:
            x = false
            self.move()
            return x

        elif self.__look.tag == Tag.ID:
            id1 = self.top.get(self.__look)

            if not id1:
                self.error(self.__look.toString() + " undeclared")

            self.move()

            if self.__look.tag != '[':
                return id1
            else:
                return self.offset(id1)

        else:
            self.error("syntax error, expected a factor, got '" + str(self.__look.tag) + "'")
            return x

    def offset(self, a):
        type1 = a.type1
        self.match('[')
        self.bool1()
        self.match(']')
        type1 = type1.of

        while self.__look.tag == '[':
            self.match('[')
            self.bool1()
            self.match(']')
            type1 = type1.of

        return Expr(Word("[]", Tag.INDEX), type1)
