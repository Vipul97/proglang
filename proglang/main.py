#!/usr/bin/env python3

from lexer import Lexer
from parser import Parser
import argparse
import json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='Path to the code file.')
    args = parser.parse_args()

    with open(args.file, 'r') as code_file:
        code = code_file.read()

    lex = Lexer(code)
    parse = Parser(lex)
    ast = parse.program()
    print(json.dumps(ast, indent=4))


if __name__ == '__main__':
    main()
