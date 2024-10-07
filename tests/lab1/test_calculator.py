import unittest
from src.lab1.calculator import *
class CalculatorTestCase(unittest.TestCase):


    def test_add(self):
        self.assertEqual(calc.add(self, 2, 3 ), 5)
    def test_sub(self):
        self.assertEqual(calc.sub(self, 10, 5), 5)
    def test_mltpl(self):
        self.asssertEqual(calc.mltpl(self, 2, 3), 6)
    def test_div(self):
        self.assertEqual(calc.div(10, 2), 5)