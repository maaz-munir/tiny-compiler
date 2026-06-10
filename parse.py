import sys
from lex import *

# parser object keeps track of current token and checks if the code matches the grammar
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

        self.symbols = set() # variables declared so far
        self.labelsDeclared = set() # labels declared so far
        self.labelsGotoed = set() # labels goto-ed so far

        self.curToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken()    # calling this twice to initialize current and peek


    # return true if current token matches
    def checkToken(self, kind):
        return kind == self.curToken.kind

    # return true if next token matches
    def checkPeek(self, kind):
        return kind == self.peekToken.kind

    # try to match current token. If not, err. Advances next token
    def match(self, kind):
        if not self.checkToken(kind):
            self.abort("expected " + kind.name + " got " + self.curToken.kind.name)

        self.nextToken()

    # advances the current token
    def nextToken(self): 
        self.curToken = self.peekToken
        self.peekToken = self.lexer.getToken()
        # No need to worry about passing the EOF, lexer handles that. // look into this.

    def abort(self, message):
        sys.exit("Error. " + message)

    
    # production rules

    # program ::= {statement}
    def program(self):
        print("PROGRAM")

        # since some newlines are required in our grammar, need to skip the excess
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()
        
        # pasre all statements in program
        while not self.checkToken(TokenType.EOF):
            self.statement()

        # check that each label referenced in a GOTO is declared
        for label in self.labelsGotoed:
            if label not in self.labelsDeclared:
                self.abort("Attempting to GOTO to undeclared label: " + label)

    def statement(self):
        # "PRINT" (expression | string)
        if self.checkToken(TokenType.PRINT):
            print("STATEMENT-PRINT")
            self.nextToken()

            if self.checkToken(TokenType.STRING):
                # simple string
                self.nextToken()
            else:
                # expects an expression
                self.expression()
        
        # "IF" comparison "THEN" {statement} "ENDIF"
        elif self.checkToken(TokenType.IF):
            print("STATEMENT-IF")
            self.nextToken()
            self.comparison()

            self.match(TokenType.THEN)
            self.nl()

            # zero or more statements in the body
            while not self.checkToken(TokenType.ENDIF):
                self.statement()
            
            self.match(TokenType.ENDIF)

        # "WHILE" comparison "REPEAT" {statement} "ENDWHILE"
        elif self.checkToken(TokenType.WHILE):
            print("STATEMENT-WHILE")
            self.nextToken()
            self.comparison()

            self.match(TokenType.REPEAT)
            self.nl()

            # Zero or more statements in the loop body.
            while not self.checkToken(TokenType.ENDWHILE):
                self.statement()

            self.match(TokenType.ENDWHILE)

        # "LABEL" ident
        elif self.checkToken(TokenType.LABEL):
            print("STATEMENT-LABEL")
            self.nextToken()

             # make sure this label doesnt already exist
            if self.curToken.text in self.labelsDeclared:
                self.abort("Label already exists: " + self.curToken.text)
            self.labelsDeclared.add(self.curToken.text)

            self.match(TokenType.IDENT)

        # "GOTO" ident
        elif self.checkToken(TokenType.GOTO):
            print("STATEMENT-GOTO")
            self.nextToken()
            self.labelsGotoed.add(self.curToken.text)
            self.match(TokenType.IDENT)

        # "LET" ident "=" expression
        elif self.checkToken(TokenType.LET):
            print("STATEMENT-LET")
            self.nextToken()

            #  checks if ident exists in symbol table. If not, declare it
            if self.curToken.text not in self.symbols:
                self.symbols.add(self.curToken.text)

            self.match(TokenType.IDENT) 
            self.match(TokenType.EQ)
            self.expression()

        # "INPUT" ident
        elif self.checkToken(TokenType.INPUT):
            print("STATEMENT-INPUT")
            self.nextToken()

            # if variable doesn't already exist, declare it
            if self.curToken.text not in self.symbols:
                self.symbols.add(self.curToken.text)

            self.match(TokenType.IDENT)

        # This is not a valid statement. Error!
        else:
            self.abort("Invalid statement at " + self.curToken.text + " (" + self.curToken.kind.name + ")")
            
        # newline.
        self.nl()


    # comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
    def comparison(self):
        print("COMPARISON")

        self.expression()

        # must be atleast one comparison operator and another expression
        if self.isComparisonOperator():
            self.nextToken()
            self.expression()
        else: 
            self.abort("expected comparison operator at: ", self.curToken.text)

        # can have 0 or more comparison operator and expressions
        while self.isComparisonOperator():
            self.nextToken()
            self.expression()


    # return true if the current token is a comparison operator
    def isComparisonOperator(self):
        return self.checkToken(TokenType.GT) or self.checkToken(TokenType.GTEQ) or self.checkToken(TokenType.LT) or self.checkToken(TokenType.LTEQ) or self.checkToken(TokenType.EQEQ) or self.checkToken(TokenType.NOTEQ)

    # expression ::= term {( "-" | "+" ) term}
    def expression(self):
        print("EXPRESSION")

        self.term()

        # can have 0 or more +/- and expressions
        while self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.nextToken()
            self.term()

    # term ::= unary {( "/" | "*" )} unary
    def term(self):
        print("TERM")

        self.unary()

        while self.checkToken(TokenType.ASTERISK) or self.checkToken(TokenType.SLASH):
            self.nextToken()
            self.unary()

    # unary ::= ["+" | "-"] primary
    def unary(self):
        print("UNARY")

        if self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.nextToken()

        self.primary()
        
    # primary ::= number | ident
    def primary(self):
        print("PRIMARY (" + self.curToken.text + ")")

        if self.checkToken(TokenType.NUMBER):
            self.nextToken()
        elif self.checkToken(TokenType.IDENT):
            # ensure variable already exists
            if self.curToken.text not in self.symbols:
                self.abort("Referencing variable before assignment: " + self.curToken.text)
            self.nextToken()

        else:
            # err
            self.abort("Unexpected token at " + self.curToken.text)


    # nl ::= '\n'+
    def nl(self):
        print("NEWLINE")
		
        # require at least one newline
        self.match(TokenType.NEWLINE)
        
        # we will allow extra newlines too
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()








    