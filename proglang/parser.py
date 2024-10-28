class Parser:
    def __init__(self, l):
        self.lex = l
        self.look = None
        self.move()

    def move(self):
        self.look = self.lex.scan()

    def error(self, s):
        raise Exception(f'near line {self.lex.line}: {s}')

    def match(self, t):
        if self.look[0] == t:
            self.move()
        else:
            self.error('syntax error')

    def program(self):
        d = self.decls()
        s = self.stmts()
        return {'type': 'program', 'decls': d, 'stmts': s}

    def block(self):
        self.match('BEGIN')
        d = self.decls()
        s = self.stmts()
        self.match('END')
        return {'type': 'block', 'decls': d, 'stmts': s}

    def decls(self):
        decls = []
        while self.look and self.look[1] in {'DEFINE', 'NUM', 'CHAR', 'BOOL', 'REAL'}:
            decls.append(self.decl())
        return decls

    def decl(self):
        if self.look[1] == 'DEFINE':
            return self.func()
        else:
            type_token = self.type_()
            id_token = self.look[1]
            self.match('ID')
            self.match(';')
            return {'type': 'decl', 'data_type': type_token[1], 'id': id_token}

    def func(self):
        self.match('DEFINE')
        return_type = self.type_()
        id_token = self.look[1]
        self.match('ID')
        self.match('(')
        params = self.params()
        self.match(')')
        block = self.block()
        return {'type': 'func', 'return_type': return_type[1], 'id': id_token, 'params': params, 'block': block}

    def type_(self):
        p = self.look
        if self.look[1] in {'NUM', 'CHAR', 'BOOL', 'REAL'}:
            self.move()
        return self.dims(p) if self.look[1] == '[' else p

    def dims(self, p):
        self.match('[')
        dimension = self.look[1]
        self.match('NUM')
        self.match(']')
        return self.dims(p) if self.look[1] == '[' else dimension, p

    def params(self):
        return self.param_list() if self.look[0] == 'ID' else []

    def param_list(self):
        params = [self.param()]
        while self.look[0] == ',':
            self.match(',')
            params.append(self.param())
        return params

    def param(self):
        type_token = self.type_()
        id_token = self.look[1]
        self.match('ID')
        return {'type': type_token[1], 'id': id_token}

    def stmts(self):
        statements = []
        while self.look != (None, None) and self.look[0] != 'END':
            statements.append(self.stmt())
        return statements

    def stmt(self):
        match self.look[1]:
            case ';':
                self.move()
                return {'type': 'empty_stmt'}

            case 'IF':
                self.match('IF')
                self.match('(')
                x = self.bool_()
                self.match(')')
                s1 = self.stmt()
                s2 = None

                if self.look[1] == 'ELSE':
                    self.match('ELSE')
                    s2 = self.stmt()

                return {'type': 'if', 'condition': x, 'then': s1, 'else': s2}

            case 'WHILE':
                self.match('WHILE')
                self.match('(')
                x = self.bool_()
                self.match(')')
                s1 = self.stmt()
                return {'type': 'while', 'condition': x, 'body': s1}

            case 'DO':
                self.match('DO')
                s1 = self.stmt()
                self.match('WHILE')
                self.match('(')
                x = self.bool_()
                self.match(')')
                self.match(';')
                return {'type': 'do', 'body': s1, 'condition': x}

            case 'BREAK':
                self.match('BREAK')
                self.match(';')
                return {'type': 'break'}

            case 'PRINT':
                self.match('PRINT')
                string_token = self.look[1]
                self.match('STRING')
                self.match(';')
                return {'type': 'print', 'value': string_token}

            case 'READ':
                self.match('READ')
                read_id = self.look[1]
                self.match('ID')
                self.match(';')
                return {'type': 'read', 'id': read_id}

            case 'BEGIN':
                return self.block()

            case 'RETURN':
                self.match('RETURN')
                value = self.bool_()
                self.match(';')
                return {'type': 'return', 'value': value}

            case _:
                return self.assign()

    def assign(self):
        id_token = self.look
        self.match('ID')

        if self.look[1] == '=':
            self.move()
            value = self.bool_()
            self.match(';')
            return {'type': 'assignment', 'id': id_token[1], 'value': value}

        elif self.look[1] == '[':
            self.offset(id_token)
            self.match('=')
            value = self.bool_()
            self.match(';')
            return {'type': 'array_access', 'id': id_token[1], 'value': value}

        elif self.look[1] == '(':
            args = self.call_stmt()
            return {'type': 'function_call', 'id': id_token[1], 'args': args}

    def offset(self, a):
        self.match('[')
        i = self.bool_()
        self.match(']')

        indices = [i]
        while self.look[1] == '[':
            self.match('[')
            i = self.bool_()
            self.match(']')
            indices.append(i)

        return {'type': 'offset', 'id': a, 'indices': indices}

    def call_stmt(self):
        self.match('(')
        args = self.arg_list()
        self.match(')')
        self.match(';')
        return {'type': 'call_stmt', 'args': args}

    def arg_list(self):
        args = []
        if self.look[1] != ')':
            args.append(self.bool_())
            while self.look[1] == ',':
                self.match(',')
                args.append(self.bool_())
        return args

    def bool_(self):
        x = self.join()
        while self.look[1] == 'OR':
            tok = self.look[1]
            self.move()
            x = {'type': 'or', 'left': x, 'op': tok, 'right': self.join()}
        return x

    def join(self):
        x = self.equality()
        while self.look[1] == 'AND':
            tok = self.look[1]
            self.move()
            x = {'type': 'and', 'left': x, 'op': tok, 'right': self.equality()}
        return x

    def equality(self):
        x = self.rel()
        while self.look[1] in {'==', '!='}:
            tok = self.look[1]
            self.move()
            x = {'type': 'equality', 'left': x, 'op': tok, 'right': self.rel()}
        return x

    def rel(self):
        x = self.expr()
        if self.look[1] in {'<', '<=', '>=', '>'}:
            tok = self.look[1]
            self.move()
            x = {'type': 'rel', 'left': x, 'op': tok, 'right': self.expr()}
        return x

    def expr(self):
        x = self.term()
        while self.look[1] in {'+', '-'}:
            tok = self.look[1]
            self.move()
            x = {'type': 'arithmetic', 'left': x, 'op': tok, 'right': self.term()}
        return x

    def term(self):
        x = self.unary()
        while self.look[1] in {'*', '/'}:
            tok = self.look[1]
            self.move()
            x = {'type': 'term', 'left': x, 'op': tok, 'right': self.unary()}
        return x

    def unary(self):
        if self.look[1] in {'-', 'NOT'}:
            tok = self.look[1]
            self.move()
            return {'type': 'unary', 'op': tok, 'operand': self.unary()}
        return self.factor()

    def factor(self):
        if self.look[1] == '(':
            self.move()
            x = self.bool_()
            self.match(')')
            return x

        elif self.look[0] in {'NUM', 'REAL'}:
            x = {'type': 'constant', 'value': self.look[1]}
            self.move()
            return x

        elif self.look[0] in {'TRUE', 'FALSE'}:
            x = {'type': 'boolean', 'value': self.look[1]}
            self.move()
            return x

        elif self.look[0] == 'STRING':
            x = {'type': 'string', 'value': self.look[1]}
            self.move()
            return x

        elif self.look[0] == 'ID':
            id_token = self.look[1]
            self.move()

            if self.look[1] != '[':
                return {'type': 'identifier', 'id': id_token}
            return {'type': 'array_access', 'id': self.offset(id_token)}

        else:
            self.error(f'syntax error')
