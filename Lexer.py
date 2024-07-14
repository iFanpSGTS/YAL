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

    def comment(self):
        result = ''
        while self.current_char is not None and self.current_char != '\n':
            result += self.current_char
            self.advance()
        return result

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
                token = Token('INTEGER', self.integer())
                print(f"Lexer: {token}")  # Log the token
                return token

            if self.current_char == '[':
                self.advance()
                token = Token('LBRACKET', '[')
                print(f"Lexer: {token}")  # Log the token
                return token

            if self.current_char == ']':
                self.advance()
                token = Token('RBRACKET', ']')
                print(f"Lexer: {token}")  # Log the token
                return token

            if self.current_char.isalpha():
                identifier = self.identifier()
                if identifier in ['if', 'while', 'for', 'print', 'println', 'else', 'fn']:
                    token = Token('KEYWORD', identifier)
                else:
                    token = Token('IDENTIFIER', identifier)
                print(f"Lexer: {token}")  # Log the token
                return token

            if self.current_char == '"' or self.current_char == "'":
                token = Token('STRING', self.string())
                print(f"Lexer: {token}")  # Log the token
                return token

            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    token = Token('OPERATOR', '==')
                else:
                    token = Token('OPERATOR', '=')
                print(f"Lexer: {token}")  # Log the token
                return token
            elif self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    token = Token('OPERATOR', '!=')
                else:
                    token = Token('OPERATOR', '!')
                print(f"Lexer: {token}")  # Log the token
                return token
            elif self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    token = Token('OPERATOR', '>=')
                else:
                    token = Token('OPERATOR', '>')
                print(f"Lexer: {token}")  # Log the token
                return token
            elif self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    token = Token('OPERATOR', '<=')
                else:
                    token = Token('OPERATOR', '<')
                print(f"Lexer: {token}")  # Log the token
                return token
            elif self.current_char == '+':
                self.advance()
                token = Token('OPERATOR', '+')
                print(f"Lexer: {token}")  # Log the token
                return token
            elif self.current_char == '-':
                self.advance()
                token = Token('OPERATOR', '-')
                print(f"Lexer: {token}")  # Log the token
                return token
            elif self.current_char == '*':
                self.advance()
                token = Token('OPERATOR', '*')
                print(f"Lexer: {token}")  # Log the token
                return token
            elif self.current_char == '/':
                self.advance()
                token = Token('OPERATOR', '/')
                print(f"Lexer: {token}")  # Log the token
                return token
            elif self.current_char == '(':
                self.advance()
                token = Token('LPAREN', '(')
                print(f"Lexer: {token}")  # Log the token
                return token
            elif self.current_char == ')':
                self.advance()
                token = Token('RPAREN', ')')
                print(f"Lexer: {token}")  # Log the token
                return token
            elif self.current_char == '{':
                self.advance()
                token = Token('LBRACE', '{')
                print(f"Lexer: {token}")  # Log the token
                return token
            elif self.current_char == '}':
                self.advance()
                token = Token('RBRACE', '}')
                print(f"Lexer: {token}")  # Log the token
                return token
            elif self.current_char == ';':
                self.advance()
                token = Token('SEMICOLON', ';')
                print(f"Lexer: {token}")  # Log the token
                return token
            elif self.current_char == ',':
                self.advance()
                token = Token('COMMA', ',')
                print(f"Lexer: {token}")  # Log the token
                return token
            elif self.current_char == '.':
                self.advance()
                token = Token('DOT', '.')
                print(f"Lexer: {token}")  # Log the token
                return token
            elif self.current_char == "#":
                self.advance()
                token = Token('COMMENT', self.comment())
                print(f"Lexer: {token}")  # Log the token
                return token
            else:
                self.error()

        token = Token('EOF', None)
        print(f"Lexer: {token}")  # Log the token
        return token

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
    with open("Example.rpl", "r") as file:
        source_code = file.read()
    tokens = tokenize(source_code)
    
    statements = parse(tokens)
    interpreter = Interpreter(statements)
    interpreter.interpret()

if __name__ == "__main__":
    main()
