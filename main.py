#!/usr/bin/env python3

from lexer.lexer import *
from parse.parser import *

if __name__ == '__main__':
    lex = Lexer()  # create lexical analyzer
    parse = Parser(lex)  # create parser
    parse.program()  # call method program in the parser

    print()
