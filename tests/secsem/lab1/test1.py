import unittest
from io import StringIO
import sys
import time
from src.secsem.lab1.task1 import logger, add, greet  

class TestLoggerDecorator(unittest.TestCase):
    def setUp(self):
        # Перехватываем stdout для проверки вывода
        self.held_output = StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_output

    def tearDown(self):
        # Восстанавливаем stdout
        sys.stdout = self.original_stdout

    def test_add_function_works_correctly(self):
        """Проверяем, что функция add работает корректно"""
        result = add(5, 2)
        self.assertEqual(result, 7)
        
        result = add(-1, -1)
        self.assertEqual(result, -2)
        
        result = add(0, 0)
        self.assertEqual(result, 0)

    def test_greet_function_works_correctly(self):
        """Проверяем, что функция greet работает корректно"""
        result = greet('maksim')
        self.assertEqual(result, 'Привет! maksim')
        
        result = greet('Anna', greet='Hello')
        self.assertEqual(result, 'Hello Anna')

    def test_logger_output_format(self):
        """Проверяем формат вывода декоратора logger"""
        add(3, 4)
        output = self.held_output.getvalue()
        
        self.assertIn("Имя функции: add", output)
        self.assertIn("Аргументы. Позиционные: (3, 4), именнованные: {}", output)
        self.assertIn("Результат: 7", output)
        self.assertIn("Время", output)

    def test_logger_with_kwargs(self):
        """Проверяем работу logger с именованными аргументами"""
        greet('Test', greet='Hi')
        output = self.held_output.getvalue()
        
        self.assertIn("Имя функции: greet", output)
        self.assertIn("Аргументы. Позиционные: ('Test',), именнованные: {'greet': 'Hi'}", output)
        self.assertIn("Результат: Hi Test", output)

    def test_logger_time_measurement(self):
        """Проверяем, что logger измеряет время выполнения"""
        @logger
        def sleep_func(seconds):
            time.sleep(seconds)
            return "done"
        
        sleep_time = 0.1 
        sleep_func(sleep_time)
        output = self.held_output.getvalue()
        
        self.assertIn("Время", output)
        
        time_line = [line for line in output.split('\n') if line.startswith('Время')][0]
        measured_time = float(time_line.split()[1])
        
        # Допускаем погрешность 20% (из-за накладных расходов)
        self.assertAlmostEqual(measured_time, sleep_time, delta=sleep_time*0.2)

    def test_logger_returns_correct_value(self):
        """Проверяем, что декоратор возвращает правильное значение"""
        @logger
        def test_func():
            return 42
            
        result = test_func()
        self.assertEqual(result, 42)

if __name__ == '__main__':
    unittest.main()