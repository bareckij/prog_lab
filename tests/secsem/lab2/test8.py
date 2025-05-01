import unittest
from unittest.mock import patch, MagicMock
import src.secsem.lab2.task8 as task8

class TestSafeIncrementCounter(unittest.TestCase):
    """Тесты для безопасного инкремента счетчика"""
    
    def setUp(self):
        """Сбрасываем счетчик перед каждым тестом"""
        task8.counter = 0
    
    def test_single_increment(self):
        """Тестирует однократный инкремент"""
        with task8.lock:
            task8.counter += 1
        self.assertEqual(task8.counter, 1)
    
    def test_safe_increment_counter(self):
        """Тестирует функцию инкремента"""
        task8.safe_increment_counter()
        self.assertEqual(task8.counter, 100000)
    
    def test_run_threads(self):
        """Тестирует полное выполнение с потоками"""
        result = task8.run_threads(thread_count=5)
        self.assertEqual(task8.counter, 500000)
        self.assertEqual(result, "Итоговое значение counter: 500000 (корректно: 500000)")
    
if __name__ == '__main__':
    unittest.main()