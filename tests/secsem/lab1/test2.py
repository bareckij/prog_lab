import unittest
from io import StringIO
import sys
from unittest.mock import patch
import random
from src.secsem.lab1.task2 import retry, risky_operation  

class TestRetryDecorator(unittest.TestCase):
    def setUp(self):
        self.held_output = StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = self.original_stdout
        random.seed()

    def test_success_on_first_attempt(self):
        """Тест успешного выполнения с первой попытки"""
        with patch('random.random', return_value=0.95):
            result = risky_operation()
            self.assertEqual(result, "Успех!")
        
        output = self.held_output.getvalue()
        self.assertEqual(output, "")

    def test_retry_mechanism(self):
        """Тест работы механизма повторных попыток"""
        random_returns = [0.1, 0.2, 0.95]  
        with patch('random.random', side_effect=random_returns):
            result = risky_operation()
            self.assertEqual(result, "Успех!")
        
        output = self.held_output.getvalue().split('\n')
        self.assertIn('Попытка 1 не удалась. Повтор через 1', output[0])
        self.assertIn('Попытка 2 не удалась. Повтор через 1', output[1])
        self.assertEqual(len(output), 3) 
    def test_all_attempts_failed(self):
        """Тест когда все попытки не удались"""
        with patch('random.random', return_value=0.1):
            result = risky_operation()
            self.assertIsNone(result) 
        
        output = self.held_output.getvalue().split('\n')
        self.assertIn('Попытка 1 не удалась. Повтор через 1', output[0])
        self.assertIn('Попытка 2 не удалась. Повтор через 1', output[1])
        self.assertIn('Все 3 попыток не удались', output[2])

    def test_specific_exceptions_only(self):
        """Тест обработки только указанных исключений"""
        @retry(attempts=2, delay=0.1, exceptions=(ValueError,))
        def test_func():
            raise TypeError("Не обрабатываемое исключение")
        
        with self.assertRaises(TypeError):
            test_func()
        
        output = self.held_output.getvalue()
        self.assertEqual(output, "")

    def test_delay_parameter(self):
        """Тест корректности работы параметра delay"""
        with patch('time.sleep') as mock_sleep:
            with patch('random.random', side_effect=[0.1, 0.95]):
                @retry(attempts=2, delay=1.5, exceptions=(ValueError,))
                def test_func():
                    if random.random() < 0.9:
                        raise ValueError
                    return "OK"
                
                result = test_func()
                self.assertEqual(result, "OK")
                
                mock_sleep.assert_called_once_with(1.5)

    def test_return_value_when_failed(self):
        """Тест что функция возвращает None при неудаче всех попыток"""
        with patch('random.random', return_value=0.1):
            result = risky_operation()
            self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()