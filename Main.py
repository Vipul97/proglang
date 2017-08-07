from lexer.Lexer import *
from parse.Parser import *


class Main:
    def main(self):
        lex = Lexer()           # create lexical analyzer
        parse = Parser(lex)     # create parser
        parse.program()         # call method program in the parser
        print '\n'

Main.main(Main())
