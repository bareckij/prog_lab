import unittest
from io import StringIO
import os 
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from lab3.task2.task2 import Survey

class TestSurvey(unittest.TestCase):

    def setUp(self):
        self.age_groups = [0, 18, 25, 35, 45, 60, 80, 100, 101]
        self.survey = Survey(self.age_groups)

    def test_add_respondent(self):
        self.survey.add_respondent('Иванов Иван Иванович', 30)
        self.assertEqual(len(self.survey.respondents), 1)
        self.assertEqual(self.survey.respondents[0], ('Иванов Иван Иванович', 30))

    def test_categorize_respondents(self):
        self.survey.add_respondent('Иванов Иван Иванович', 30)
        self.survey.add_respondent('Петров Петр Петрович', 70)
        self.survey.add_respondent('Сидоров Сидор Сидорович', 105)
        
        with StringIO() as captured_output:
            sys.stdout = captured_output
            self.survey.categorize_respondents()
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue().strip()
        
        expected_output = """101-inf: Сидоров Сидор Сидорович (105)
60-80: Петров Петр Петрович (70)
25-35: Иванов Иван Иванович (30)"""
        
        self.assertEqual(output, expected_output)

    def test_duplicate_respondents(self):
        self.survey.add_respondent('Иванов Иван Иванович', 30)
        self.survey.add_respondent('Иванов Иван Иванович', 30)
        
        self.assertEqual(len(self.survey.respondents), 2)

    def test_group_order(self):
        """Тестируем корректность сортировки групп по возрасту."""
        self.assertEqual(self.survey.get_group_order('80-100'), 100)
        self.assertEqual(self.survey.get_group_order('101-inf'), 101)
        self.assertEqual(self.survey.get_group_order('25-35'), 35)

if __name__ == "__main__":
    unittest.main()
