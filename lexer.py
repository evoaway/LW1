import re

FLOAT = 'FLOAT'
INTEGER = 'INTEGER'
ASSIGN = 'ASSIGN'
ID = 'ID'
LPAR = 'LPAR'
RPAR = 'RPAR'
PLUS = 'PLUS'
MINUS = 'MINUS'
MULT = 'MULT'
DIV = 'DIV'
NEWLINE = 'NEWLINE'
SKIP = 'SKIP'
MISMATCH = 'MISMATCH'
UNARY_MINUS = 'UNARY_MINUS'
BIN = 'BIN'
OCT = 'OCT'
HEX = 'HEX'
SHORT_FLOAT = 'SHORT_FLOAT'

TOKEN_TYPE = [
    (BIN, r'0b[01]+'),
    (OCT, r'0o[0-7]+'),
    (HEX, r'0x[a-fA-F0-9]+'),
    (FLOAT, r'\d+\.\d*([eE][-+]?\d+)?|\d*\.\d+([eE][-+]?\d+)?|\d+[eE][-+]?\d+'),
    #(SHORT_FLOAT, r'\.\d(\d)*([eE][-+]?\d+)?'),
    (INTEGER, r'\d+'),
    (ASSIGN, r'='),
    (ID, r'[A-Za-z]+'),
    (LPAR, r'\('),
    (RPAR, r'\)'),
    (PLUS, r'\+'),
    (MINUS, r'-'),
    (MULT, r'\*'),
    (DIV, r'\/'),
    (UNARY_MINUS,  r'-'),
    (NEWLINE, r'\n'),
    (SKIP, r'[ \t]+'),
    (MISMATCH, r'.'),
]

operations = {PLUS, MINUS, MULT, DIV}
unary_ops = {PLUS, MINUS}
numbers = {INTEGER, FLOAT, SHORT_FLOAT}
not_dec_numbers = {BIN, OCT, HEX}
keywords = {'if', 'else'}

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column


class Lexer:
    def __init__(self, code):
        self.code = code

    def analysis(self):
        tokens = []
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_TYPE)
        line_num = 1
        line_start = 0
        for m in re.finditer(tok_regex, self.code):
            type = m.lastgroup
            value = m.group()
            column = m.start() - line_start
            if type == INTEGER:
                if len(value) > 1 and value.startswith('0'):
                    raise ValueError("Leading zeros are forbidden")
            if type == FLOAT:
                if len(value) > 1 and value.startswith('00'):
                    raise ValueError("Leading zeros are forbidden")
            if type in not_dec_numbers:
                num = value[2:]
                if len(num) > 1 and num.startswith('0'):
                    raise ValueError("Leading zeros are forbidden")
            if type == 'NEWLINE':
                line_start = m.end()
                line_num += 1
                continue
            elif type == 'SKIP':
                continue
            elif type == 'MISMATCH':
                raise RuntimeError(f'Unexpected token on position {line_num},{column}')
            tokens.append(Token(type, value, line_num, column))
        return tokens

text = "1e5+2.3e-4-1.23+646846+0+.5"
for token in Lexer(text).analysis():
    print(token.value, '->', token.type)