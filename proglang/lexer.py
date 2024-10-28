class Lexer:
    def __init__(self, code):
        self.code = code
        self.line = 1
        self.peek = None
        self.current_index = 0
        self.keywords = {
            'DEFINE',
            'BEGIN',
            'END',
            'OR',
            'AND',
            'NOT',
            'IF',
            'ELSE',
            'WHILE',
            'DO',
            'BREAK',
            'PRINT',
            'READ',
            'RETURN',
            'TRUE',
            'FALSE'
        }

    def readch(self):
        if self.current_index < len(self.code):
            self.peek = self.code[self.current_index]
            self.current_index += 1
        else:
            self.peek = None

    def handle_comment(self):
        self.readch()
        if self.peek == '/':
            while self.peek and self.peek != '\n':
                self.readch()
            self.line += 1
        elif self.peek == '*':
            while True:
                self.readch()
                if self.peek is None:
                    raise SyntaxError('Missing "*/"')
                elif self.peek == '\n':
                    self.line += 1
                elif self.peek == '*':
                    self.readch()
                    if self.peek == '/':
                        break

    def handle_operator(self):
        op = self.peek
        self.readch()
        if op in {'=', '!', '<', '>'} and self.peek == '=':
            return op + self.peek, op + self.peek
        self.current_index -= 1
        return op, op

    def handle_number(self):
        v = 0
        while self.peek.isdigit():
            v = 10 * v + int(self.peek)
            self.readch()

        if self.peek != '.':
            self.current_index -= 1
            return 'NUM', v

        x = v
        d = 10
        while True:
            self.readch()
            if not self.peek.isdigit():
                break
            x += float(self.peek) / d
            d *= 10

        self.current_index -= 1
        return 'REAL', x

    def handle_identifier(self):
        s = self.peek
        self.readch()

        while self.peek and self.peek.isalnum():
            s += self.peek
            self.readch()

        self.current_index -= 1
        return (s, s) if s in self.keywords else ('ID', s)

    def handle_string(self):
        s = ''
        if self.peek == '"':
            self.readch()
            while self.peek and self.peek != '"':
                s += self.peek
                self.readch()
                if self.peek is None:
                    raise SyntaxError('Missing "\""')
        return 'STRING', s

    def scan(self):
        while True:
            self.readch()

            if self.peek in {' ', '\t'}:
                continue
            elif self.peek == '\n':
                self.line += 1
            elif self.peek == '/':
                self.handle_comment()
            else:
                break

        if self.peek:
            if self.peek in {'&', '|', '=', '!', '<', '>'}:
                return self.handle_operator()
            elif self.peek.isdigit():
                return self.handle_number()
            elif self.peek.isalpha():
                return self.handle_identifier()
            elif self.peek == '"':
                return self.handle_string()

        tok = self.peek
        self.peek = None
        return tok, tok
