class Statement:
    pass

class Expression:
    pass

class IfStatement(Statement):
    def __init__(self, condition, true_statements, false_statements):
        self.condition = condition
        self.true_statements = true_statements
        self.false_statements = false_statements

    def __str__(self):
        return f"IfStatement({self.condition}, {self.true_statements}, {self.false_statements})"

    def __repr__(self):
        return self.__str__()

class WhileStatement(Statement):
    def __init__(self, condition, statements):
        self.condition = condition
        self.statements = statements

    def __str__(self):
        return f"WhileStatement({self.condition}, {self.statements})"

    def __repr__(self):
        return self.__str__()

class ForStatement(Statement):
    def __init__(self, identifier, start, condition, step, statements):
        self.identifier = identifier
        self.start = start
        self.condition = condition
        self.step = step
        self.statements = statements

    def __str__(self):
        return f"ForStatement({self.identifier}, {self.start}, {self.condition}, {self.step}, {self.statements})"

    def __repr__(self):
        return self.__str__()

class PrintStatement(Statement):
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        return f"PrintStatement({self.expression})"

    def __repr__(self):
        return self.__str__()

class AssignmentStatement(Statement):
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

    def __str__(self):
        return f"AssignmentStatement({self.identifier}, {self.value})"

    def __repr__(self):
        return self.__str__()

class BinaryExpression(Expression):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self):
        return f"BinaryExpression({self.left}, {self.operator}, {self.right})"

    def __repr__(self):
        return self.__str__()

class UnaryExpression(Expression):
    def __init__(self, operator, expression):
        self.operator = operator
        self.expression = expression

    def __str__(self):
        return f"UnaryExpression({self.operator}, {self.expression})"

    def __repr__(self):
        return self.__str__()

class IntegerLiteral(Expression):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"IntegerLiteral({self.value})"

    def __repr__(self):
        return self.__str__()

class Identifier(Expression):
    def __init__(self, identifier):
        self.identifier = identifier

    def __str__(self):
        return f"Identifier({self.identifier})"

    def __repr__(self):
        return self.__str__()

class StringLiteral(Expression):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'StringLiteral("{self.value}")'

    def __repr__(self):
        return self.__str__()

class FunctionStatement(Statement):
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body

    def __str__(self):
        return f"FunctionStatement({self.name}, {self.parameters}, {self.body})"

    def __repr__(self):
        return self.__str__()

class FunctionCall(Expression):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

    def __str__(self):
        return f"FunctionCall({self.name}, {self.arguments})"

    def __repr__(self):
        return self.__str__()
