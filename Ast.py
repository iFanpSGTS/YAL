from Statement import (
    IfStatement, WhileStatement, ForStatement, PrintStatement, AssignmentStatement,
    BinaryExpression, UnaryExpression, IntegerLiteral, Identifier, StringLiteral
)
from ErrorHandler import LexerError, ParserError, InterpreterError

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_pos = 0
        self.current_token = self.tokens[self.current_pos]

    def advance(self):
        self.current_pos += 1
        if self.current_pos < len(self.tokens):
            self.current_token = self.tokens[self.current_pos]
        else:
            self.current_token = None

    def parse(self):
        statements = []
        while self.current_token is not None:
            if self.current_token.type == 'KEYWORD':
                if self.current_token.value == 'if':
                    statements.append(self.parse_if())
                elif self.current_token.value == 'while':
                    statements.append(self.parse_while())
                elif self.current_token.value == 'for':
                    statements.append(self.parse_for())
                elif self.current_token.value in ['print', 'println']:
                    statements.append(self.parse_print())
            elif self.current_token.type == 'IDENTIFIER':
                statements.append(self.parse_assignment())
            else:
                self.advance()
        return statements

    def parse_if(self):
        self.advance()
        if self.current_token.type == 'LPAREN':
            self.advance()
            condition = self.parse_expression()
            if self.current_token.type == 'RPAREN':
                self.advance()
                if self.current_token.type == 'LBRACE':
                    self.advance()
                    true_statements = self.parse_statements()
                    if self.current_token.type == 'RBRACE':
                        self.advance()
                        false_statements = []
                        if self.current_token is not None and self.current_token.type == 'KEYWORD' and self.current_token.value == 'else':
                            self.advance()
                            if self.current_token.type == 'LBRACE':
                                self.advance()
                                false_statements = self.parse_statements()
                                if self.current_token.type == 'RBRACE':
                                    self.advance()
                                else:
                                    raise ParserError("Expected RBRACE")
                            else:
                                raise ParserError("Expected LBRACE")
                        return IfStatement(condition, true_statements, false_statements)
                    else:
                        raise ParserError("Expected RBRACE")
                else:
                    raise ParserError("Expected LBRACE")
            else:
                raise ParserError("Expected RPAREN")
        else:
            raise ParserError("Expected LPAREN")

    def parse_while(self):
        self.advance()
        if self.current_token.type == 'LPAREN':
            self.advance()
            condition = self.parse_expression()
            if self.current_token.type == 'RPAREN':
                self.advance()
                if self.current_token.type == 'LBRACE':
                    self.advance()
                    statements = self.parse_statements()
                    if self.current_token.type == 'RBRACE':
                        self.advance()
                        return WhileStatement(condition, statements)
                    else:
                        raise ParserError("Expected RBRACE")
                else:
                    raise ParserError("Expected LBRACE")
            else:
                raise ParserError("Expected RPAREN")
        else:
            raise ParserError("Expected LPAREN")

    def parse_for(self):
        self.advance()
        if self.current_token.type == 'LPAREN':
            self.advance()
            if self.current_token.type == 'IDENTIFIER':
                identifier = self.current_token.value
                self.advance()
                if self.current_token.type == 'OPERATOR' and self.current_token.value == '=':
                    self.advance()
                    start = self.parse_expression()
                    if self.current_token.type == 'SEMICOLON':
                        self.advance()
                        condition = self.parse_expression()
                        if self.current_token.type == 'SEMICOLON':
                            self.advance()
                            step = self.parse_expression()
                            if self.current_token.type == 'RPAREN':
                                self.advance()
                                if self.current_token.type == 'LBRACE':
                                    self.advance()
                                    statements = self.parse_statements()
                                    if self.current_token.type == 'RBRACE':
                                        self.advance()
                                        return ForStatement(identifier, start, condition, step, statements)
                                    else:
                                        raise ParserError("Expected RBRACE")
                                else:
                                    raise ParserError("Expected LBRACE")
                            else:
                                raise ParserError("Expected RPAREN")
                        else:
                            raise ParserError("Expected SEMICOLON")
                    else:
                        raise ParserError("Expected SEMICOLON")
                else:
                    raise ParserError("Expected OPERATOR")
            else:
                raise ParserError("Expected IDENTIFIER")
        else:
            raise ParserError("Expected LPAREN")

    def parse_print(self):
        self.advance()
        if self.current_token.type == 'LPAREN':
            self.advance()
            expression = self.parse_expression()
            if self.current_token.type == 'RPAREN':
                self.advance()
                if self.current_token.type == 'SEMICOLON':
                    self.advance()
                    return PrintStatement(expression)
                else:
                    raise ParserError("Expected SEMICOLON")
            else:
                raise ParserError("Expected RPAREN")
        else:
            raise ParserError("Expected LPAREN")

    def parse_assignment(self):
        identifier = self.current_token.value
        self.advance()
        if self.current_token.type == 'OPERATOR' and self.current_token.value == '=':
            self.advance()
            value = self.parse_expression()
            if self.current_token.type == 'SEMICOLON':
                self.advance()
                return AssignmentStatement(identifier, value)
            else:
                raise ParserError("Expected SEMICOLON")
        else:
            raise ParserError("Expected OPERATOR")

    def parse_expression(self):
        return self.parse_binary()

    def parse_binary(self):
        left = self.parse_unary()
        while self.current_token.type == 'OPERATOR':
            operator = self.current_token.value
            self.advance()
            right = self.parse_unary()
            left = BinaryExpression(left, operator, right)
        return left

    def parse_unary(self):
        if self.current_token.type == 'OPERATOR':
            operator = self.current_token.value
            self.advance()
            return UnaryExpression(operator, self.parse_unary())
        else:
            return self.parse_primary()

    def parse_primary(self):
        if self.current_token.type == 'INTEGER':
            value = self.current_token.value
            self.advance()
            return IntegerLiteral(value)
        elif self.current_token.type == 'IDENTIFIER':
            identifier = self.current_token.value
            self.advance()
            return Identifier(identifier)
        elif self.current_token.type == 'STRING':
            value = self.current_token.value
            self.advance()
            return StringLiteral(value)
        elif self.current_token.type == 'LPAREN':
            self.advance()
            expression = self.parse_expression()
            if self.current_token.type == 'RPAREN':
                self.advance()
                return expression
            else:
                raise ParserError("Expected RPAREN")
        else:
            raise ParserError("Expected INTEGER, IDENTIFIER, or STRING")

    def parse_statements(self):
        statements = []
        while self.current_token is not None and self.current_token.type != 'RBRACE':
            statement = self.parse_statement()
            if statement is not None:
                statements.append(statement)
        return statements

    def parse_statement(self):
        if self.current_token.type == 'KEYWORD' and self.current_token.value == 'if':
            return self.parse_if()
        elif self.current_token.type == 'KEYWORD' and self.current_token.value == 'while':
            return self.parse_while()
        elif self.current_token.type == 'KEYWORD' and self.current_token.value == 'for':
            return self.parse_for()
        elif self.current_token.type == 'KEYWORD' and self.current_token.value in ['print', 'println']:
            return self.parse_print()
        elif self.current_token.type == 'IDENTIFIER':
            return self.parse_assignment()
        elif self.current_token.type == 'SEMICOLON':
            self.advance()
            return None
        else:
            raise ParserError(f"Expected KEYWORD or IDENTIFIER but got {self.current_token}")

class Interpreter:
    def __init__(self, statements):
        self.statements = statements
        self.variables = {}

    def interpret(self):
        for statement in self.statements:
            self.execute(statement)

    def execute(self, statement):
        if isinstance(statement, IfStatement):
            self.execute_if(statement)
        elif isinstance(statement, WhileStatement):
            self.execute_while(statement)
        elif isinstance(statement, ForStatement):
            self.execute_for(statement)
        elif isinstance(statement, PrintStatement):
            self.execute_print(statement)
        elif isinstance(statement, AssignmentStatement):
            self.execute_assignment(statement)
        else:
            raise InterpreterError(f"Unknown statement type: {type(statement)}")

    def evaluate(self, expression):
        if isinstance(expression, IntegerLiteral):
            return expression.value
        elif isinstance(expression, StringLiteral):
            return expression.value
        elif isinstance(expression, Identifier):
            return self.variables.get(expression.identifier, 0)
        elif isinstance(expression, BinaryExpression):
            left = self.evaluate(expression.left)
            right = self.evaluate(expression.right)
            if expression.operator == '+':
                if isinstance(left, str) or isinstance(right, str):
                    return str(left) + str(right)
                return left + right
            elif expression.operator == '-':
                return left - right
            elif expression.operator == '*':
                return left * right
            elif expression.operator == '/':
                return left / right
            elif expression.operator == '>':
                return left > right
            elif expression.operator == '<':
                return left < right
            elif expression.operator == '==':
                return left == right
            elif expression.operator == '!=':
                return left != right
            elif expression.operator == '>=':
                return left >= right
            elif expression.operator == '<=':
                return left <= right
            elif expression.operator == '=':
                if isinstance(expression.left, Identifier):
                    self.variables[expression.left.identifier] = right
                    return right
                else:
                    raise InterpreterError("Left side of assignment must be an identifier")
            else:
                raise InterpreterError(f"Unknown operator: {expression.operator}")
        elif isinstance(expression, UnaryExpression):
            value = self.evaluate(expression.expression)
            if expression.operator == '-':
                return -value
            else:
                raise InterpreterError(f"Unknown operator: {expression.operator}")
        else:
            raise InterpreterError(f"Unknown expression type: {type(expression)}")

    def execute_if(self, statement):
        condition = self.evaluate(statement.condition)
        if condition:
            for stmt in statement.true_statements:
                self.execute(stmt)
        else:
            for stmt in statement.false_statements:
                self.execute(stmt)

    def execute_while(self, statement):
        while self.evaluate(statement.condition):
            for stmt in statement.statements:
                self.execute(stmt)

    def execute_for(self, statement):
        self.variables[statement.identifier] = self.evaluate(statement.start)
        while self.evaluate(statement.condition):
            for stmt in statement.statements:
                self.execute(stmt)
            self.variables[statement.identifier] = self.evaluate(statement.step)

    def execute_print(self, statement):
        value = self.evaluate(statement.expression)
        print(value)

    def execute_assignment(self, statement):
        self.variables[statement.identifier] = self.evaluate(statement.value)