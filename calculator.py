import operator
import lexer
import math_functions


class TextCalculator:
    def __init__(self):
        self.operations = {
            'PLUS': operator.add,
            'MINUS': operator.sub,
            'MULT': operator.mul,
            'DIV': operator.truediv,
            'UNARY_MINUS': operator.neg
        }
        self.precedence = {'PLUS': 1, 'MINUS': 1, 'MULT': 2, 'DIV': 2, 'UNARY_MINUS': 3}
        self.var_expression = {}
        self.var_value = {}
        self.visited = set()

    def shunting_yard(self, tokens):
        output_queue = []
        operator_stack = []
        previous_token = None

        for token in tokens:
            if token.type in lexer.numbers:
                output_queue.append(math_functions.str_to_num(token))
            
            elif token.type in lexer.not_dec_numbers:
                output_queue.append(token)
            
            elif token.type == lexer.ID:
                output_queue.append(token)

            elif token.type in lexer.operations:
                if token.type == lexer.MINUS:
                    if previous_token is None or previous_token.type in lexer.operations or previous_token.type == lexer.LPAR:
                        token.type = lexer.UNARY_MINUS
                while (operator_stack and operator_stack[-1] != lexer.LPAR and
                       self.precedence.get(operator_stack[-1].type, 0) >= self.precedence.get(token.type, 0)):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)

            elif token.type == lexer.LPAR:
                operator_stack.append(token)

            elif token.type == lexer.RPAR:
                while operator_stack and operator_stack[-1].type != lexer.LPAR:
                    output_queue.append(operator_stack.pop())
                if not operator_stack or operator_stack[-1].type != lexer.LPAR:
                    raise ValueError("Mismatched parentheses")
                operator_stack.pop()
            previous_token = token

        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                raise ValueError("Mismatched parentheses")
            output_queue.append(op)

        return output_queue

    def evaluate(self, tokens):
        result_stack = []

        for token in tokens:
            if token.type in lexer.numbers:
                result_stack.append(token.value)
            elif token.type in lexer.not_dec_numbers:
                result_stack.append(math_functions.to_dec(token.value, token.type))
            elif token.type == lexer.UNARY_MINUS:
                if len(result_stack) < 1:
                    raise ValueError(f"Operator '{token.value}' requires 1 operand")
                a = result_stack.pop()
                result = self.operations[token.type](a)
                result_stack.append(result)
            # elif token.type in lexer.unary_ops:
            #     if len(result_stack) > 1:
            #         operand2 = result_stack.pop()
            #         operand1 = result_stack.pop()
            #         result = self.operations[token.type](operand1, operand2)
            #         result_stack.append(result)
            #     else:
            #         operand = result_stack.pop()
            #         result_stack.append(self.operations[token.type](0, operand))
            elif token.type in lexer.operations:
                if len(result_stack) < 2:
                    raise ValueError(f"Operator '{token.value}' requires 2 operands")
                operand2 = result_stack.pop()
                operand1 = result_stack.pop()
                result = self.operations[token.type](operand1, operand2)
                result_stack.append(result)
            elif token.type == lexer.ID:
                result_stack.append(self.evaluate_variable(token.value))
            else:
                raise ValueError(f"Unknown token : {token.value} on position {token.column}")

        if len(result_stack) != 1:
            raise ValueError("Invalid expression structure")
        return result_stack[0]

    def evaluate_variable(self, variable):
        if variable in self.var_value:
            return self.var_value[variable]

        if variable in self.visited:
            raise RecursionError(f"Circular dependency detected for '{variable}'")

        if variable not in self.var_expression:
            raise NameError(f"Variable '{variable}' is not defined")

        self.visited.add(variable)

        try:
            expression = self.var_expression[variable]
            tokens = lexer.Lexer(expression).analysis()
            tokens_queue = self.shunting_yard(tokens)
            result = self.evaluate(tokens_queue)
            self.var_value[variable] = result

            return result
        finally:
            self.visited.remove(variable)

    def evaluate_expression(self, expression, base):
        tokens = lexer.Lexer(expression).analysis()
        tokens_queue = self.shunting_yard(tokens)
        result = self.evaluate(tokens_queue)

        if base == 10:
            return result

        if isinstance(result, int):
            return math_functions.convert_int_to_base(result, base)
        return math_functions.convert_float_to_base(result, base)


    def get_expression(self, variable):
        if variable not in self.var_expression:
            raise NameError(f"Variable '{variable}' is not defined")

        return self.var_expression[variable]

    def variable_assignment(self, variable, expression):
        # if variable in self.var_value:
        #     del self.var_value[variable]
        self.var_value = {}
        self.var_expression[variable] = expression

    def clear(self):
        self.var_value = {}
        self.var_expression = {}
