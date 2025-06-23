import re

# Визначення типів токенів та їх регулярних виразів
# Порядок важливий: числа з плаваючою комою повинні йти перед цілими,
# щоб уникнути неправильного розпізнавання (напр., "3.14" як ціле "3").
token_specification = [
    ('FLOAT',     r'\d+\.\d*([eE][-+]?\d+)?|\d*\.\d+([eE][-+]?\d+)?|\d+[eE][-+]?\d+'), # Числа з плаваючою комою
    ('INTEGER',   r'\d+'),                                     # Цілі числа
    ('VARIABLE',  r'[a-zA-Z_][a-zA-Z0-9_]*'),                    # Змінні
    ('PLUS',      r'\+'),                                       # Знак додавання
    ('MINUS',     r'-'),                                       # Знак віднімання
    ('MULTIPLY',  r'\*'),                                       # Знак множення
    ('DIVIDE',    r'/'),                                       # Знак ділення
    ('ASSIGN',    r'='),                                       # Знак присвоєння
    ('LPAREN',    r'\('),                                       # Ліва дужка
    ('RPAREN',    r'\)'),                                       # Права дужка
    ('WHITESPACE',r'\s+'),                                      # Пробіли (для ігнорування)
    ('MISMATCH',  r'.'),                                        # Будь-який інший символ (помилка)
]

# Створення єдиного регулярного виразу для пошуку токенів
tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)

def lexical_analyzer(code):
    """
    Функція лексичного аналізатора.
    Приймає рядок коду та повертає генератор токенів.
    """
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'WHITESPACE':
            continue  # Ігноруємо пробільні символи
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Несподіваний символ: {value}')
        yield kind, value

# Приклад використання
if __name__ == "__main__":
    input_code = "position = initial + rate * 60.5e-2"

    print(f"Вхідний рядок: \"{input_code}\"\n")
    print("Результат лексичного аналізу:")
    print("-" * 30)
    print(f"{'Тип токена':<12} | {'Значення'}")
    print("-" * 30)

    try:
        for token in lexical_analyzer(input_code):
            print(f"{token[0]:<12} | {token[1]}")
    except RuntimeError as e:
        print(e)

    print("\n" + "="*30 + "\n")

    # Ще один приклад з різними формами чисел
    input_code_2 = "var_1 = .5 + 100 - 12e+4 / -2"
    print(f"Вхідний рядок: \"{input_code_2}\"\n")
    print("Результат лексичного аналізу:")
    print("-" * 30)
    print(f"{'Тип токена':<12} | {'Значення'}")
    print("-" * 30)
    try:
        for token in lexical_analyzer(input_code_2):
            print(f"{token[0]:<12} | {token[1]}")
    except RuntimeError as e:
        print(e)