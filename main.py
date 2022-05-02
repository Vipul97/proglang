from lexer.lexer import *
from parse.parser import *


class Main:
    def main(self):
        lex = Lexer()  # create lexical analyzer
        parse = Parser(lex)  # create parser
        parse.program()  # call method program in the parser
        print()


Main.main(Main())
