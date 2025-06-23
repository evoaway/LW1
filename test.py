import unittest
from calculator import TextCalculator
from main import process_input


class TestFunctions(unittest.TestCase):
    def test_simple_expression(self):
        calculator = TextCalculator()
        line = "((51+28)*56)-7"
        result = process_input(line, calculator)
        self.assertEqual(result, "= 4417")

    def test_get_var_value(self):
        calculator = TextCalculator()
        line = "a=0.5+.5+5e1/10"
        process_input(line, calculator)
        line = "a"
        result = process_input(line, calculator)
        self.assertEqual(result, "= 6.0")

    def test_get_var_expression(self):
        calculator = TextCalculator()
        line = "a=0.5+.5+5.0e1/10"
        process_input(line, calculator)
        line = "?a"
        result = process_input(line, calculator)
        self.assertEqual(result, "a = 0.5+.5+5.0e1/10")

    def test_var_is_not_defined(self):
        calculator = TextCalculator()
        line = "a=5*(1.5+2)"
        process_input(line, calculator)
        line = "b"
        error_res = process_input(line, calculator)
        self.assertEqual(error_res, "Error: Variable 'b' is not defined")

    def test_circular_dependency(self):
        calculator = TextCalculator()
        line = "a=b+1"
        process_input(line, calculator)
        line = "b=a"
        process_input(line, calculator)
        line = "b"
        error_res = process_input(line, calculator)
        self.assertEqual(error_res, "Error: Circular dependency detected for 'b'")

    def test_bin_oct_hex_simple_exp(self):
        calculator = TextCalculator()
        line = "a=0b1+0o2+0xa"
        process_input(line, calculator)
        line = "a"
        result = process_input(line, calculator)
        self.assertEqual(result, "= 13")

    def test_bin_oct_hex_division(self):
        calculator = TextCalculator()
        line = "(-0b1 / -0o2 + 0xa) + 1.0e1 =>2"
        result = process_input(line, calculator)
        self.assertEqual(result, "= 0b10100.1")

    def test_leading_zero(self):
        calculator = TextCalculator()
        line = "0b00101"
        error_res = process_input(line, calculator)
        self.assertEqual(error_res, "Error: Leading zeros are forbidden")

if __name__ == '__main__':
    unittest.main()