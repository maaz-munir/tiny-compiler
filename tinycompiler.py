from lex import *
from parse import *
from emit import *
import sys

def main():
    print("Tiny Compiler")

    if len(sys.argv) != 2:
        sys.exit("error: compiler needs source file as argument")

    with open(sys.argv[1], 'r') as inputFile:
        source = inputFile.read()

    # init lexer, parser and emitter
    lexer = Lexer(source)
    emitter = Emitter("out.c")
    parser = Parser(lexer, emitter)

    parser.program() # start parser
    emitter.writeFile() # write the output to file

    print("compiling completed")

if __name__ == "__main__":
    main()