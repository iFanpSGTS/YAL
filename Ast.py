from Statement import (
    IfStatement, WhileStatement, ForStatement, PrintStatement, AssignmentStatement,
    BinaryExpression, UnaryExpression, IntegerLiteral, Identifier, StringLiteral, FunctionStatement, FunctionCall
)
from ErrorHandler import LexerError, ParserError, InterpreterError

class ArrayLiteral:
    def __init__(self, elements):
        self.elements = elements
    
    def append(self, element):
        self.elements.append(element)
        return None

class MethodCall:
    def __init__(self, object_name, method_name, arguments):
        self.object_name = object_name
        self.method_name = method_name
        self.arguments = arguments

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
                elif self.current_token.value == 'fn':
                    statements.append(self.parse_function())
            elif self.current_token.type == 'IDENTIFIER':
                statements.append(self.parse_assignment_or_function_call())
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
    ...

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
                            # print(step)
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
                            raise ParserError("Expected SEMICOLON after step")
                    else:
                        raise ParserError("Expected SEMICOLON after condition")
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
                # print(self.current_token)
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

    def parse_function(self):
        self.advance()  
        if self.current_token.type == 'IDENTIFIER':
            name = self.current_token.value
            self.advance()  
            if self.current_token.type == 'LPAREN':
                self.advance()  
                parameters = []
                while self.current_token.type != 'RPAREN':
                    if self.current_token.type == 'IDENTIFIER':
                        parameters.append(self.current_token.value)
                        # print(parameters)
                        self.advance()
                        if self.current_token.type == 'COMMA':
                            self.advance()  
                    else:
                        raise ParserError("Expected IDENTIFIER or RPAREN")
                if self.current_token.type == 'RPAREN':
                    self.advance()  
                    if self.current_token.type == 'LBRACE':
                        self.advance()  
                        body = self.parse_statements()
                        if self.current_token.type == 'RBRACE':
                            self.advance()  
                            return FunctionStatement(name, parameters, body)
                        else:
                            raise ParserError("Expected RBRACE")
                    else:
                        raise ParserError("Expected LBRACE")
                else:
                    raise ParserError("Expected RPAREN")
            else:
                raise ParserError("Expected LPAREN")
        else:
            raise ParserError("Expected IDENTIFIER")

    def parse_assignment_or_function_call(self):
        identifier = self.current_token.value
        self.advance()
        if self.current_token.type == 'OPERATOR' and self.current_token.value == '=':
            self.advance()
            value = self.parse_expression()
            if self.current_token.type == 'SEMICOLON':
                self.advance()
                return AssignmentStatement(identifier, value)
        elif self.current_token.type == 'LPAREN':
            self.advance()
            arguments = []
            while self.current_token.type != 'RPAREN':
                arguments.append(self.parse_expression())
                if self.current_token.type == 'COMMA':
                    self.advance()
                # print(arguments)
            if self.current_token.type == 'RPAREN':
                self.advance()
                if self.current_token.type == 'SEMICOLON':
                    self.advance()
                    return FunctionCall(identifier, arguments)
                else:
                    raise ParserError("Expected SEMICOLON")
            else:
                raise ParserError("Expected RPAREN")
        elif self.current_token.type == 'DOT':
            self.advance()
            method = self.current_token.value
            self.eat('IDENTIFIER')
            if self.current_token.type == 'LPAREN':
                self.eat('LPAREN')
                arguments = []
                while self.current_token.type != 'RPAREN':
                    arguments.append(self.parse_expression())
                    if self.current_token.type == 'COMMA':
                        self.eat('COMMA')
                self.eat('RPAREN')
                if self.current_token.type == 'SEMICOLON':
                    self.eat('SEMICOLON')
                    return MethodCall(identifier, method, arguments)
                else:
                    raise ParserError("Expected SEMICOLON")
            else:
                raise ParserError("Expected LPAREN")
        else:
            raise ParserError("Expected OPERATOR or LPAREN")

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

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.advance()
        else:
            raise ParserError(f"Expected token type {token_type} but got {self.current_token.type}")

    def parse_primary(self):
        token = self.current_token
        if token.type == 'INTEGER':
            self.eat('INTEGER')
            return IntegerLiteral(token.value)
        elif token.type == 'IDENTIFIER':
            self.eat('IDENTIFIER')
            if self.current_token.type == 'DOT':
                self.eat('DOT')
                method = self.current_token.value
                self.eat('IDENTIFIER')
                if self.current_token.type == 'LPAREN':
                    self.eat('LPAREN')
                    arguments = []
                    while self.current_token.type != 'RPAREN':
                        arguments.append(self.parse_expression())
                        if self.current_token.type == 'COMMA':
                            self.eat('COMMA')
                    self.eat('RPAREN')
                    return MethodCall(token.value, method, arguments)
            return Identifier(token.value)
        elif token.type == 'STRING':
            self.eat('STRING')
            return StringLiteral(token.value)
        elif token.type == 'LBRACKET':
            self.eat('LBRACKET')
            elements = []
            while self.current_token.type != 'RBRACKET':
                elements.append(self.parse_expression())
                if self.current_token.type == 'COMMA':
                    self.eat('COMMA')
            self.eat('RBRACKET')
            return ArrayLiteral(elements)
        else:
            print(f"Unhandled token: {token}")
            raise ParserError("Expected INTEGER, IDENTIFIER, STRING, or LBRACKET")


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
        elif self.current_token.type == 'KEYWORD' and self.current_token.value == 'fn':
            return self.parse_function()
        elif self.current_token.type == 'IDENTIFIER':
            return self.parse_assignment_or_function_call()
        elif self.current_token.type == 'SEMICOLON':
            self.advance()
            return None
        else:
            raise ParserError(f"Expected KEYWORD or IDENTIFIER but got {self.current_token}")

class Interpreter:
    def __init__(self, statements):
        self.statements = statements
        self.variables = {}
        self.functions = {}

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
        elif isinstance(statement, FunctionStatement):
            self.execute_function(statement)
        elif isinstance(statement, FunctionCall):
            self.execute_function_call(statement)
        elif isinstance(statement, MethodCall):
            self.execute_method_call(statement)
        else:
            raise InterpreterError(f"Unknown statement type: {type(statement)}")

    def execute_method_call(self, statement):
        obj = self.variables.get(statement.object_name)
        if obj is None:
            raise InterpreterError(f"Object {statement.object_name} not defined")
        if statement.method_name == 'count':
            if isinstance(obj, str):
                return len(obj)
            elif isinstance(obj, list):
                return len(obj)
            elif isinstance(obj, dict):
                return len(obj)
            else:
                raise InterpreterError(f"Object {statement.object_name} is not a string, list, or dictionary")
        method = getattr(obj, statement.method_name, None)
        if method is None:
            raise InterpreterError(f"Method {statement.method_name} not found on object {statement.object_name}")
        arguments = [self.evaluate(arg) for arg in statement.arguments]
        try:
            return method(*arguments)
        except Exception as e:
            raise InterpreterError(f"Error executing method {statement.method_name} on object {statement.object_name}: {e}")

    def evaluate(self, expression):
        if isinstance(expression, IntegerLiteral):
            return expression.value
        elif isinstance(expression, StringLiteral):
            return expression.value
        elif isinstance(expression, Identifier):
            return self.variables.get(expression.identifier, 0)
        elif isinstance(expression, ArrayLiteral):
            return [self.evaluate(element) for element in expression.elements]
        elif isinstance(expression, MethodCall):
            return self.execute_method_call(expression)
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
        # print(statement.identifier)
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

    def execute_function(self, statement):
        self.functions[statement.name] = statement

    def execute_function_call(self, statement):
        function = self.functions.get(statement.name)
        if function is None:
            raise InterpreterError(f"Function {statement.name} not defined")
        
        local_variables = self.variables.copy()
        if len(function.parameters) != len(statement.arguments):
            raise InterpreterError(f"Function {statement.name} expects {len(function.parameters)} arguments but got {len(statement.arguments)}")
        for param, arg in zip(function.parameters, statement.arguments):
            local_variables[param] = self.evaluate(arg)

        original_variables = self.variables
        self.variables = local_variables
        try:
            for stmt in function.body:
                self.execute(stmt)
        finally:
            self.variables = original_variables
