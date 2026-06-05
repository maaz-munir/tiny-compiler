import enum
import sys

class Lexer:
    def __init__(self, source):
        # source code to lex as a string. Append a newline to simplify lexing/parsing the last token/statement
        self.source = source + '\n'
        
        self.curChar = '' # current character in the str

        self.curPos = -1 # current position in the string

        self.nextChar()


    # process the next character
    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = '\0' # EOF / end of file
        else:
            self.curChar = self.source[self.curPos]

    # return the lookahead character
    def peek(self):
        if self.curPos + 1 >= len(self.source):
            return '\0'
        else:
            return self.source[self.curPos + 1]
    # invalid token found, print error message and exit
    def abort(self, message):
        sys.exit("lexing error " + message)

    # skip whitespace except except newlines, which we will use to indicate the end of a statement
    def skipWhitespace(self):
        while self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r':
            self.nextChar()

    # skip comments
    def skipComments(self):
        if self.curChar == "#":
            while self.curChar != '\n':
                self.nextChar()

    # return the next token
    def getToken(self):
        self.skipWhitespace()
        self.skipComments()

        token = None

        # check the first character of this token to see if we can decide what it is
        # if multiple char operator (e.g., !=) , number, identifier, or keyword then process the rest
        if self.curChar == '+':
            token = Token(self.curChar, TokenType.PLUS)
        elif self.curChar == '-':
            token = Token(self.curChar, TokenType.MINUS)
        elif self.curChar == '/':
            token = Token(self.curChar, TokenType.SLASH)
        elif self.curChar == '*':
            token = Token(self.curChar, TokenType.ASTERISK)
        elif self.curChar == '\n':
            token = Token(self.curChar, TokenType.NEWLINE)
        elif self.curChar == '\0':
            token = Token('', TokenType.EOF)
        elif self.curChar == "=":
            if self.peek() == "=": # meaning ==
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.EQEQ)
            else:
                token = Token(self.curChar, TokenType.EQ)
        elif self.curChar == '>':
            if self.peek() == '=': # >=
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.GTEQ)
            else: # >
                token = Token(self.curChar, TokenType.GT)
        
        elif self.curChar == '<':
                if self.peek() == '=': # <=
                    lastChar = self.curChar
                    self.nextChar()
                    token = Token(lastChar + self.curChar, TokenType.LTEQ)
                else: # <
                    token = Token(self.curChar, TokenType.LT)

        elif self.curChar == '!':
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.NOTEQ)
            else:
                self.abort("Expected !=, got !" + self.peek())

        elif self.curChar == '\"': # strings
            self.nextChar()
            startPos = self.curPos

            while self.curChar != '\"':
                # cant allow special characters. No escape characters, newlines, tabs, or %
                if self.curChar == '\r' or self.curChar == '\n' or self.curChar == '\t' or self.curChar == '\\' or self.curChar == '%':
                    self.abort("Illegal character in string.")
                self.nextChar()

            tokenText = self.source[startPos: self.curPos]
            token = Token(tokenText, TokenType.STRING)

        elif self.curChar.isdigit():
            startPos = self.curPos
            while self.peek().isdigit():
                self.nextChar()
            if self.peek() == ".": 
                self.nextChar()

                if not self.peek().isdigit():
                    self.abort("illegal character in number")
                
                while self.peek().isdigit():
                    self.nextChar()
            
            tokenText = self.source[startPos: self.curPos +1]
            token = Token(tokenText, TokenType.NUMBER)

        elif self.curChar.isalpha():
            startPos = self.curPos

            while self.peek().isalnum():
                self.nextChar()

            tokenText = self.source[startPos: self.curPos+1]
            keyword = Token.checkIfKeyword(tokenText)
            if keyword == None:
                token = Token(tokenText, TokenType.IDENT)
            else:
                token = Token(tokenText, keyword)


        else:
            self.abort("unknown token: " + self.curChar)
        
        self.nextChar()
        return token



class Token():
    def __init__(self, tokenText, tokenKind):
        self.text = tokenText # the actual token text itself
        self.kind = tokenKind # the token type that the token is classified as e.g number, keyword etc

    @staticmethod
    def checkIfKeyword(tokenText):
        for kind in TokenType:
            # this relies on our keywords having enums b/w 100 and 200(1XX) in TokenType 
            if kind.name == tokenText and kind.value >= 100 and kind.value < 200:
                return kind
        return None

# TokenType is our enum for all the types of tokens.
class TokenType(enum.Enum):
	EOF = -1
	NEWLINE = 0
	NUMBER = 1
	IDENT = 2
	STRING = 3
	
    # Keywords.
	LABEL = 101
	GOTO = 102
	PRINT = 103
	INPUT = 104
	LET = 105
	IF = 106
	THEN = 107
	ENDIF = 108
	WHILE = 109
	REPEAT = 110
	ENDWHILE = 111
	
    # Operators.
	EQ = 201  
	PLUS = 202
	MINUS = 203
	ASTERISK = 204
	SLASH = 205
	EQEQ = 206
	NOTEQ = 207
	LT = 208
	LTEQ = 209
	GT = 210
	GTEQ = 211