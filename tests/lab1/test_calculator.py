import unittest
from src.lab1.calculator import calc
class CalculatorTestCase(unittest.TestCase):
    def test_add(self):
        self.assertEqual(calc.add(self, 2, 3 ), 5.0)
    def test_sub(self):
        self.assertEqual(calc.sub(self, 10, 5), 5.0)
    def test_mltpl(self):
        self.assertEqual(calc.mltpl(self, 2, 3), 6.0)
    def test_div(self):
        self.assertEqual(calc.div(self, 10, 2), 5.0)