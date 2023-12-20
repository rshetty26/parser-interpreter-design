class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __eq__(self, other):
        if isinstance(other, Token):
            return self.type == other.type and self.value == other.value
        return False

    def __repr__(self):
        return f'Token({self.type}, {self.value})'


class Lexer:
    def __init__(self, input):
        self.input = input
        self.position = 0

    def tokenize(self):
        returnList = []
        while self.position < len(self.input):
            x = self.input[self.position]
            if x.isalpha():
                val = ''
                while self.position < len(self.input) and (self.input[self.position].isalpha() or self.input[self.position].isnumeric()):
                    val += self.input[self.position]
                    self.position += 1
                returnList.append(Token("VARIABLE", val))
            elif x.isnumeric():
                val = ''
                while self.position < len(self.input) and self.input[self.position].isnumeric():
                    val += self.input[self.position]
                    self.position += 1
                returnList.append(Token("INTEGER", int(val)))
            else:
                if x == "=":
                    returnList.append(Token("ASSIGN", x))
                elif x == ";":
                    returnList.append(Token("SEMICOLON", x))
                elif x == "(" or x == ")":
                    returnList.append(Token("PARENTHESIS", x))
                elif x == "+" or x == "-" or x == "*" or x == "/":
                    returnList.append(Token("OPERATOR", x))
                elif x == " " or x == "\n":
                    pass
                else:
                    raise Exception('Syntax Error: Invalid character')
                self.position += 1
        return returnList

class Node:
    def __init__(self, type, value=None, children=None):
        self.type = type
        self.value = value
        self.children = children if children is not None else []

    def __str__(self, level=0):
        ret = "\t" * level + f'{self.type}: {self.value}\n'
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def consume(self, expected_type = None):
        if self.position < len(self.tokens):
            if self.tokens[self.position].type == expected_type or expected_type is None:
                self.position += 1
                return self.tokens[self.position-1]
            else:
                raise Exception('Syntax error')
        else:
            raise Exception('Syntax error: unexpected end of input')

    def peek(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def parse(self):
        root = Node("Assignment")
        while self.position < len(self.tokens):
            root.children.append(self.parse_statement())
        return root

    def parse_statement(self):
        if self.peek() and self.peek().type == "VARIABLE":
            return self.parse_assignment()
        else:
            raise Exception("Syntax error")

    def parse_assignment(self):
        variable = self.consume("VARIABLE")
        self.consume("ASSIGN")
        expressions = []
        while self.peek() and not self.peek().type == "SEMICOLON":
            expressions.append(self.parse_expression())
        self.consume("SEMICOLON")
        return Node("Variable", variable.value, expressions)

    def parse_expression(self):
        if self.peek() and self.peek().type == "(":
            self.consume("PARENTHESIS")
            first = self.parse_expression()
            operator = self.consume("OPERATOR")
            last = self.parse_term()
            last.consume("PARENTHESIS")
            return Node("Operator", operator.value, [first, last])
        else:
            if self.peek() and self.peek().type == "OPERATOR":
                return Node("Operator", self.consume("OPERATOR").value, [self.parse_term()]) 
            else:
                first = self.parse_term()
                if self.peek() and self.peek().type == "OPERATOR":
                    operator = self.consume("OPERATOR")
                    last = self.parse_term()
                    return Node("Operator", operator.value, [first, last])
                return first

    def parse_term(self):
        if self.peek() and self.peek().type == "INTEGER":
            return Node("INTEGER", self.consume("INTEGER").value)
        elif self.peek() and self.peek().type == "VARIABLE":
            return Node("Variable", self.consume("VARIABLE").value)
        elif self.peek() and self.peek().type == "PARENTHESIS":
            self.consume("PARENTHESIS")
            expression = self.parse_expression()
            self.consume("PARENTHESIS")
            return expression
        else:
            raise Exception('Syntax error')

