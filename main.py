import re
from calculator import TextCalculator

def process_input(line, calculator):
    if not line:
        return None

    base = 10
    separator = '=>'
    line = line.strip()
    if len(line.split(separator)) == 2:
        line, base = line.split(separator)
        if base in ['2', '8', '16']:
            base = int(base)
        else:
            return f"Error: Invalid or unsupported base '{base}'"

    if line.startswith('?'):
        query = line[1:].strip()
        if not query: return "Error: Empty query"
        try:
            #result = calculator.get_variable(query, base)
            result = calculator.get_expression(query)
            return f"{query} = {result}"
        except Exception as e:
            return f"Error: {e}"
    if '=' in line:
        parameters = line.split('=')
        variable = parameters[0].strip()
        expression = parameters[1].strip()
        if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', variable):
            return f"Error: Invalid variable name '{variable}'"

        try:
            calculator.variable_assignment(variable, expression)
        except Exception as e:
            return f"Error: {e}"
    else:
        try:
            result = calculator.evaluate_expression(line, base)
            return f"= {result}"
        except Exception as e:
            return f"Error: {e}"

def run_calculator():
    print("Enter expressions ((51+28)*56)-7=), assignments (S = 18), queries var expression (?S) of value (S). Type 'q' to end")
    print("-" * 60)
    calculator = TextCalculator()

    while True:
        try:
            line = input("> ")
        except EOFError:
            print("\nExiting")
            break

        line = line.strip()
        if not line:
            continue

        if line.lower() == 'q':
            print("Exiting")
            break

        if line.lower() == 'clear':
            calculator.clear()
            continue

        result = process_input(line, calculator)
        if result:
            print(result)

if __name__ == "__main__":
        run_calculator()