import unittest
from unittest.mock import patch, MagicMock
import threading
import time
import sys
from io import StringIO

from src.secsem.lab2.task7 import counter, increment_counter  

class TestIncrementCounter(unittest.TestCase):
    """Тесты для функции increment_counter"""
    
    def setUp(self):
        """Сбрасываем счетчик перед каждым тестом"""
        global counter
        counter = 0
    
    @patch('time.sleep', return_value=None)
    def test_increment_counter_race_condition(self, mock_sleep):
        """Тестирует наличие race condition при инкременте"""
        global counter
        
        # Создаем 5 потоков
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=increment_counter)
            thread.start()
            threads.append(thread)
        
        # Ждем завершения всех потоков
        for thread in threads:
            thread.join()
        
        # Проверяем что итоговое значение меньше ожидаемого (из-за race condition)
        self.assertLess(counter, 500000)
        print(f"\nФактическое значение: {counter} (ожидалось 500000)")


class TestThreadSafetySolutions(unittest.TestCase):                                                                                                                                                                                                                                                                                                                                                  
    """Тесты различных решений проблемы race condition"""
    
    def setUp(self):
        """Сбрасываем счетчик перед каждым тестом"""
        global counter
        counter = 0
    
    @patch('time.sleep', return_value=None)
    def test_with_lock_solution(self, mock_sleep):
        """Тестирует решение с использованием Lock"""
        global counter
        lock = threading.Lock()
        
        def safe_increment():
            global counter
            for _ in range(100000):
                with lock:
                    temp = counter
                    temp += 1
                    time.sleep(0.000001)
                    counter = temp
        
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=safe_increment)
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()
        
        self.assertEqual(counter, 500000)

if __name__ == '__main__':
    unittest.main()