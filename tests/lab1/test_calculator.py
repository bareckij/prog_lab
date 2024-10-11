import unittest
from src.lab1.calculator import _calc
class CalculatorTestCase(unittest.TestCase):
    def test_add(self):
        self.assertEqual(_calc.add(self, 2, 3 ), 5.0)
    def test_sub(self):
        self.assertEqual(_calc.sub(self, 10, 5), 5.0)
    def test_mltpl(self):
        self.assertEqual(_calc.mltpl(self, 2, 3), 6.0)
    def test_div(self):
        self.assertEqual(_calc.div(self, 10, 2), 5.0)