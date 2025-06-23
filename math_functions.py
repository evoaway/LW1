import lexer


def str_to_num(num_token):
    if num_token.type == lexer.INTEGER:
        num_token.value = int(num_token.value)
    else:
        num_token.value = float(num_token.value)
    return num_token

def to_dec(value, type):
    if type == 'BIN':
        return int(value, 2)
    elif type == 'OCT':
        return int(value, 8)
    return int(value, 16)

def convert_int_to_base(value, base):
    if base == 2:
        return bin(value)
    if base == 8:
        return oct(value)
    if base == 16:
        return hex(value)

def convert_fractional(fractional_part, base, precision):
    if not (0 <= fractional_part < 1):
        raise ValueError("Input must be a positive fractional number less than 1")

    result = ""
    hex_chars = "0123456789ABCDEF"

    for _ in range(precision):
        fractional_part *= base
        integer_part = int(fractional_part)

        if base == 16:
            result += hex_chars[integer_part]
        else:
            result += str(integer_part)

        fractional_part -= integer_part
        if fractional_part == 0:
            break

    return result

def convert_float_to_base(value, base, precision=10):
    integer_part = int(value)
    fractional_part = abs(value - integer_part)

    if base == 2:
        integer_str = bin(integer_part)
    elif base == 8:
        integer_str = oct(integer_part)
    elif base == 16:
        integer_str = hex(integer_part)

    if fractional_part == 0:
        return integer_str

    fractional_str = convert_fractional(fractional_part, base, precision)

    return f"{integer_str}.{fractional_str}"
