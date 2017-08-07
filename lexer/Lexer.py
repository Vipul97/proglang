from lexer.Word import *
from symbols.Type import *
from lexer.Num import *
from lexer.Real import *

code = open("lexer/code.txt", 'r')


class Lexer:
    line = 1
    peek = ' '
    words = {}

    def reserve(self, w):
        self.words[w.lexeme] = w

    def __init__(self):
        self.reserve(Word("DEFINE",     Tag.DEFINE))
        self.reserve(Word("RECORD",     Tag.RECORD))
        self.reserve(Word("BEGIN",      Tag.BEGIN))
        self.reserve(Word("END",        Tag.END))
        self.reserve(Word("OR",         Tag.OR))
        self.reserve(Word("AND",        Tag.AND))
        self.reserve(Word("NOT",        Tag.NOT))
        self.reserve(Word("IF",         Tag.IF))
        self.reserve(Word("ELSE",       Tag.ELSE))
        self.reserve(Word("WHILE",      Tag.WHILE))
        self.reserve(Word("DO",         Tag.DO))
        self.reserve(Word("BREAK",      Tag.BREAK))
        self.reserve(Word("PRINT",      Tag.PRINT))
        self.reserve(Word("READ",       Tag.READ))
        self.reserve(Word("RETURN",     Tag.RETURN))
        self.reserve(TRUE)
        self.reserve(FALSE)
        self.reserve(NUM)
        self.reserve(CHAR)
        self.reserve(BOOL)
        self.reserve(REAL)

    def readch(self, c=None):
        if c is None:
            self.peek = code.read(1)

        else:
            self.readch()
            if self.peek != c:
                return False

            self.peek = ' '
            return True

    def scan(self):
        while True:
            self.readch()

            if self.peek == '/':
                self.peek = code.read(1)
                if self.peek == '/':
                    while not self.readch('\n'):
                        continue
                    self.line += 1

                elif self.peek == '*':
                    while True:
                        self.peek = code.read(1)
                        if not self.peek:
                            print "Syntax Error: Missing '*/'"
                            exit()
                        elif self.peek == '\n':
                            self.line += 1
                        elif self.peek == '*':
                            if self.readch('/'):
                                break

            if self.peek == '"':
                while not self.readch('"'):
                    if not self.peek:
                        print "Syntax Error: Missing '\"'"
                        exit()

            if self.peek == ' ' or self.peek == '\t':
                continue
            elif self.peek == '\n':
                self.line += 1
            else:
                break

        if self.peek == '&':
            return Token('&')

        elif self.peek == '|':
            return Token('|')

        elif self.peek == '=':
            if self.readch('='):
                return eq
            else:
                code.seek(code.tell() - 1)
                return Token('=')

        elif self.peek == '!':
            if self.readch('='):
                return ne
            else:
                code.seek(code.tell() - 1)
                return Token('!')

        elif self.peek == '<':
            if self.readch('='):
                return le
            else:
                code.seek(code.tell() - 1)
                return Token('<')

        elif self.peek == '>':
            if self.readch('='):
                return ge
            else:
                code.seek(code.tell() - 1)
                return Token('>')

        if self.peek.isdigit():
            v = 0

            v = 10 * v + int(self.peek)
            self.readch()

            while self.peek.isdigit():
                v = 10 * v + int(self.peek)
                self.readch()

            if self.peek != '.':
                code.seek(code.tell() - 1)
                return Num(v)

            x = v
            d = 10

            while True:
                self.readch()

                if not self.peek.isdigit():
                    break

                x += float(self.peek) / d
                d *= 10

            code.seek(code.tell() - 1)
            return Real(x)

        if self.peek.isalpha():
            s = self.peek
            self.readch()

            while self.peek.isalpha() or self.peek.isdigit():
                s += self.peek
                self.readch()

            code.seek(code.tell() - 1)
            if s in self.words:
                w = self.words[s]
                return w

            w = Word(s, Tag.ID)
            self.words[s] = w
            return w

        tok = Token(self.peek)
        self.peek = ' '
        return tok
