import asyncio
import unittest
from unittest.mock import patch
from io import StringIO
import sys
from src.secsem.lab2.task1 import delayed_message, main  


class TestDelayedMessage(unittest.IsolatedAsyncioTestCase):
    """Тесты для функции delayed_message"""
    
    @patch('sys.stdout', new_callable=StringIO)
    async def test_delayed_message_output(self, mock_stdout):
        """Тестирует вывод сообщения после задержки"""
        test_message = "Test message"
        test_delay = 0.1  #Небольшую задержку для тестов
        
        await delayed_message(test_message, test_delay)
        
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, test_message)
    
    async def test_delayed_message_awaits(self):
        """Тестирует, что функция действительно ожидает указанное время"""
        test_delay = 0.5
        start_time = asyncio.get_event_loop().time()
        
        await delayed_message("Test", test_delay)
        
        end_time = asyncio.get_event_loop().time()
        elapsed = end_time - start_time
        self.assertGreaterEqual(elapsed, test_delay)

class TestMainFunction(unittest.IsolatedAsyncioTestCase):
    """Тесты для функции main"""
    
    @patch('sys.stdout', new_callable=StringIO)
    async def test_main_output(self, mock_stdout):
        """Тестирует правильную последовательность вывода в main"""
        expected_output = """Начало работы
Сообщение после 2 секунд
Конец работы
"""
        
        await main()
        
        output = mock_stdout.getvalue()
        self.assertEqual(output, expected_output)
    


class TestIntegration(unittest.IsolatedAsyncioTestCase):
    """Интеграционные тесты"""
    
    @patch('sys.stdout', new_callable=StringIO)
    async def test_full_flow(self, mock_stdout):
        """Тестирует полный поток выполнения с моком времени"""
        with patch('asyncio.sleep', return_value=None) as mock_sleep:
            await main()
            
            mock_sleep.assert_called_once_with(2)
            
            output = mock_stdout.getvalue().splitlines()
            self.assertEqual(output[0], "Начало работы")
            self.assertEqual(output[1], "Сообщение после 2 секунд")
            self.assertEqual(output[2], "Конец работы")

if __name__ == '__main__':
    unittest.main()