import unittest
from unittest.mock import patch, MagicMock, call
import time
import threading
from io import StringIO
import sys
from src.secsem.lab2.task6 import print_message 

class TestPrintMessage(unittest.TestCase):
    """Тесты для функции print_message"""
    
    @patch('time.sleep')
    @patch('builtins.print')
    def test_print_message(self, mock_print, mock_sleep):
        """Тестирует что функция ждет указанное время и печатает сообщение"""
        print_message("Test message", 2)
        
        mock_sleep.assert_called_once_with(2)
        mock_print.assert_called_once_with("Test message")

class TestExecutionModes(unittest.TestCase):
    """Тесты для последовательного и параллельного выполнения"""
    
    @patch('time.sleep')
    @patch('builtins.print')
    def test_sequential_execution(self, mock_print, mock_sleep):
        """Тестирует последовательное выполнение"""
        messages = ["Msg1", "Msg2", "Msg3"]
        delay = 2
        
        with patch('time.time', side_effect=[0, 2, 4, 6, 6]):
            # Тестируем последовательное выполнение
            for msg in messages:
                print_message(msg, delay)
            
            # Проверяем вызовы sleep
            self.assertEqual(mock_sleep.call_count, 3)
            mock_sleep.assert_has_calls([call(2), call(2), call(2)])
            
            # Проверяем вывод сообщений
            mock_print.assert_has_calls([call("Msg1"), call("Msg2"), call("Msg3")])
    
    @patch('time.sleep')
    @patch('builtins.print')
    @patch('threading.Thread')
    def test_parallel_execution(self, mock_thread, mock_print, mock_sleep):
        """Тестирует параллельное выполнение в потоках"""
        messages = ["Msg1", "Msg2", "Msg3"]
        delay = 2
        
        # Настраиваем моки потоков
        mock_thread_instances = [MagicMock() for _ in messages]
        mock_thread.side_effect = mock_thread_instances
        
        # Фиксируем время выполнения
        with patch('time.time', side_effect=[0, 0, 0, 0, 2, 2]):
            threads = []
            for msg in messages:
                thread = threading.Thread(target=print_message, args=(msg, delay))
                thread.start()
                threads.append(thread)
            
            for thread in threads:
                thread.join()
            
            # Проверяем что потоки были созданы и запущены
            self.assertEqual(mock_thread.call_count, 3)
            for instance in mock_thread_instances:
                instance.start.assert_called_once()
                instance.join.assert_called_once()
    

if __name__ == '__main__':
    unittest.main()