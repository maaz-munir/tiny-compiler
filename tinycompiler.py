from lex import *
from parse import *
import sys

def main():
    print("Tiny Compiler")

    if len(sys.argv) != 2:
        sys.exit("error: compiler needs source file as argument")

    with open(sys.argv[1], 'r') as inputFile:
        source = inputFile.read()

    # init lexer and parser
    lexer = Lexer(source)
    parser = Parser(lexer)

    parser.program() # start parser
    print("parsing completed")

if __name__ == "__main__":
    main()