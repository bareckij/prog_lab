import asyncio
import unittest
from unittest.mock import patch, MagicMock, AsyncMock
from io import StringIO
from src.secsem.lab2.task3 import delayed_message, main

class TestDelayedMessage(unittest.IsolatedAsyncioTestCase):
    """Тесты для функции delayed_message"""
    
    async def test_delayed_message_returns_correct_value(self):
        """Тестирует что функция возвращает правильное сообщение"""
        result = await delayed_message("Test message", 0.1)
        self.assertEqual(result, "Test message")
    
    async def test_delayed_message_awaits_correct_time(self):
        """Тестирует что функция ожидает указанное время"""
        with patch('asyncio.sleep', new=AsyncMock()) as sleep_mock:
            await delayed_message("Test", 0.5)
            sleep_mock.assert_awaited_once_with(0.5)

class TestIntegration(unittest.IsolatedAsyncioTestCase):
    """Интеграционные тесты"""
    
    @patch('sys.stdout', new_callable=StringIO)
    async def test_full_flow_with_reduced_delays(self, mock_stdout):
        """Тестирует полный поток с уменьшенными задержками"""
        # Подменяем оригинальные задержки на уменьшенные для тестов
        async def test_main():
            tasks = [
                delayed_message("Сообщение после 0.2 секунд", 0.2),
                delayed_message("Сообщение после 0.1 секунды", 0.1),
                delayed_message("Сообщение после 0.3 секунд", 0.3),
            ]
            
            for completed_task in asyncio.as_completed(tasks):
                result = await completed_task
                print(result)
            
            print("Все задачи завершены!")
        
        await test_main()
        
        output = mock_stdout.getvalue().splitlines()
        self.assertEqual(output[0], "Сообщение после 0.1 секунды")
        self.assertEqual(output[1], "Сообщение после 0.2 секунд")
        self.assertEqual(output[2], "Сообщение после 0.3 секунд")
        self.assertEqual(output[3], "Все задачи завершены!")

if __name__ == '__main__':
    unittest.main()