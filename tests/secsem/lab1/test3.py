import unittest
from io import StringIO
import sys
import time
from unittest.mock import patch
from src.secsem.lab1.task3 import logger 

class TestLoggerDecorator(unittest.TestCase):
    def setUp(self):
        self.held_output = StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_output

    def tearDown(self):
        # Восстанавливаем stdout
        sys.stdout = self.original_stdout

    def test_regular_method_logging(self):
        """Тест логирования обычного метода"""
        @logger(show=True)
        class TestClass:
            def test_method(self, a, b):
                return a + b

        obj = TestClass()
        result = obj.test_method(2, 3)
        
        self.assertEqual(result, 5)
        
        output = self.held_output.getvalue()
        self.assertIn("Имя класса TestClass", output)
        self.assertIn("Имя метода test_method", output)
        self.assertIn("Аргументы.(2, 3)", output)
        self.assertIn("Время выполнения", output)
        self.assertIn("Результат 5", output)

    def test_magic_method_logging_when_enabled(self):
        """Тест логирования магических методов при show=True"""
        @logger(show=True)
        class TestClass:
            def __str__(self):
                return "TestClass instance"

        obj = TestClass()
        result = str(obj)
        
        self.assertEqual(result, "TestClass instance")
        
        output = self.held_output.getvalue()
        self.assertIn("Имя метода __str__", output)

    def test_magic_method_no_logging_when_disabled(self):
        """Тест что магические методы не логируются при show=False"""
        @logger(show=False)
        class TestClass:
            def __str__(self):
                return "TestClass instance"

        obj = TestClass()
        result = str(obj)
        
        self.assertEqual(result, "TestClass instance")
        
        output = self.held_output.getvalue()
        self.assertEqual(output, "")

    def test_init_method_logging(self):
        """Тест логирования метода __init__"""
        @logger(show=True)
        class TestClass:
            def __init__(self, value):
                self.value = value

        obj = TestClass(10)
        
        self.assertEqual(obj.value, 10)
        
        output = self.held_output.getvalue()
        self.assertIn("Имя метода __init__", output)
        self.assertIn("Аргументы.(10,)", output)

    def test_time_measurement(self):
        """Тест измерения времени выполнения"""
        @logger(show=True)
        class TestClass:
            def sleep_method(self, seconds):
                time.sleep(seconds)
                return "done"

        with patch('time.sleep'):
            obj = TestClass()
            obj.sleep_method(0.1)
        
        output = self.held_output.getvalue()
        self.assertIn("Время выполнения", output)
        
    def test_multiple_methods_logging(self):
        """Тест что все методы класса задекорированы"""
        @logger(show=True)
        class TestClass:
            def method1(self):
                return 1
            
            def method2(self):
                return 2

        obj = TestClass()
        obj.method1()
        obj.method2()
        
        output = self.held_output.getvalue()
        self.assertIn("Имя метода method1", output)
        self.assertIn("Имя метода method2", output)

if __name__ == '__main__':
    unittest.main()