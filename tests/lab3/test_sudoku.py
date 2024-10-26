import unittest
import src.lab3.sudoku as sudoku
class CalculatorTestCase(unittest.TestCase):
    def test_sudoku(self):
        self.assertEqual(sudoku.group([1,2,3,4,5], 3), [[1,2,3],[4,5]])