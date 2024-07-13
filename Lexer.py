from Statement import (
    IfStatement, WhileStatement, ForStatement, PrintStatement, AssignmentStatement,
    BinaryExpression, UnaryExpression, IntegerLiteral, Identifier, StringLiteral
)
from ErrorHandler import LexerError, ParserError, InterpreterError
from Ast import Parser, Interpreter

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.current_pos = 0
        self.current_char = self.source_code[self.current_pos]
        self.tokens = []

    def error(self):
        raise LexerError("Invalid character")

    def advance(self):
        self.current_pos += 1       
        if self.current_pos < len(self.source_code):
            self.current_char = self.source_code[self.current_pos]        
        else:            
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def identifier(self):
        result = ''
        while self.current_char is not None and self.current_char.isalpha():
            result += self.current_char
            self.advance()
        return result

    def string(self):
        result = ''
        self.advance()
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        self.advance()
        return result

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token('INTEGER', self.integer())

            if self.current_char.isalpha():
                identifier = self.identifier()
                if identifier in ['if', 'while', 'for', 'print', 'println', 'else']:
                    return Token('KEYWORD', identifier)
                else:
                    return Token('IDENTIFIER', identifier)

            if self.current_char == '"':
                return Token('STRING', self.string())

            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token('OPERATOR', '==')
                else:
                    return Token('OPERATOR', '=')
            elif self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token('OPERATOR', '!=')
                else:
                    return Token('OPERATOR', '!')
            elif self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token('OPERATOR', '>=')
                else:
                    return Token('OPERATOR', '>')
            elif self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token('OPERATOR', '<=')
                else:
                    return Token('OPERATOR', '<')
            elif self.current_char == '+':
                self.advance()
                return Token('OPERATOR', '+')
            elif self.current_char == '-':
                self.advance()
                return Token('OPERATOR', '-')
            elif self.current_char == '*':
                self.advance()
                return Token('OPERATOR', '*')
            elif self.current_char == '/':
                self.advance()
                return Token('OPERATOR', '/')
            elif self.current_char == '(':
                self.advance()
                return Token('LPAREN', '(')
            elif self.current_char == ')':
                self.advance()
                return Token('RPAREN', ')')
            elif self.current_char == '{':
                self.advance()
                return Token('LBRACE', '{')
            elif self.current_char == '}':
                self.advance()
                return Token('RBRACE', '}')
            elif self.current_char == ';':
                self.advance()
                return Token('SEMICOLON', ';')
            elif self.current_char == ',':
                self.advance()
                return Token('COMMA', ',')
            else:
                self.error()

        return Token('EOF', None)

    def tokenize(self):
        while True:
            token = self.get_next_token()
            if token.type == 'EOF':
                break
            self.tokens.append(token)
        return self.tokens

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"Token({self.type}, {self.value})"

    def __repr__(self):
        return self.__str__()

def tokenize(source_code):
    lexer = Lexer(source_code)
    return lexer.tokenize()

def parse(tokens):
    parser = Parser(tokens)
    return parser.parse()

def main():
    source_code = """
    for (i = 0; i < 5; i = i + 1) {
        println("i is " + i);
    }
    """
    tokens = tokenize(source_code)
    statements = parse(tokens)
    interpreter = Interpreter(statements)
    interpreter.interpret()

if __name__ == "__main__":
    main()