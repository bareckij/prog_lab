import unittest
from unittest.mock import patch, MagicMock
import time
import threading
from io import StringIO
import sys
from src.secsem.lab2.task5 import print_with_delay 

class TestPrintWithDelay(unittest.TestCase):
    """Тесты для функции print_with_delay"""
    
    @patch('time.sleep')
    @patch('builtins.print')
    def test_print_with_delay(self, mock_print, mock_sleep):
        """Тестирует что функция ждет 2 секунды и печатает сообщение"""
        print_with_delay("Test message")
        
        # Проверяем что sleep был вызван с правильным временем
        mock_sleep.assert_called_once_with(2)
        
        # Проверяем что print был вызван с правильным сообщением
        mock_print.assert_called_once_with("Test message")

class TestThreadExecution(unittest.TestCase):
    """Тесты для работы с потоками"""
    
    @patch('time.sleep')
    @patch('builtins.print')
    def test_thread_creation(self, mock_print, mock_sleep):
        
        """Тестирует создание и запуск потока"""
        # Заменяем реальную функцию на mock
        with patch('threading.Thread') as mock_thread:
            mock_thread_instance = MagicMock()
            mock_thread.return_value = mock_thread_instance
            
            # Запускаем тестируемый код
            thread = threading.Thread(target=print_with_delay, args=("Test message",))
            thread.start()
            thread.join()
            
            # Проверяем что поток был создан и запущен
            mock_thread.assert_called_once_with(target=print_with_delay, args=("Test message",))
            mock_thread_instance.start.assert_called_once()
            mock_thread_instance.join.assert_called_once()
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_full_execution_flow(self, mock_stdout):
        """Тестирует полный поток выполнения"""
        # Мокируем sleep чтобы не ждать реальные 2 секунды
        with patch('time.sleep', return_value=None):
            # Создаем и запускаем поток
            thread = threading.Thread(target=print_with_delay, args=("Сообщение после 2 секунд",))
            thread.start()
            
            # Печатаем сообщение из основного потока
            print("Основной поток продолжает работу...")
            
            thread.join()
            print("Поток завершил работу.")
            
            # Получаем весь вывод
            output = mock_stdout.getvalue().strip().split('\n')
            
            # Проверяем порядок вывода (может варьироваться из-за многопоточности)
            self.assertIn("Основной поток продолжает работу...", output)
            self.assertIn("Сообщение после 2 секунд", output)
            self.assertIn("Поток завершил работу.", output)

if __name__ == '__main__':
    unittest.main()