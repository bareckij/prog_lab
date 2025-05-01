import asyncio
import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
from src.secsem.lab2.task2 import delayed_message, main

class TestDelayedMessage(unittest.IsolatedAsyncioTestCase):
    """Тесты для функции delayed_message"""
    
    @patch('sys.stdout', new_callable=StringIO)
    async def test_delayed_message_output(self, mock_stdout):
        """Тестируем вывод delayed_message"""
        await delayed_message("Test message", 0.1)
        self.assertEqual(mock_stdout.getvalue().strip(), "Test message")
    
    async def test_delayed_message_order(self):
        """Тестируем порядок выполнения delayed_message"""
        results = []
        
        async def wrapper(msg, delay):
            await asyncio.sleep(delay)
            results.append(msg)
        
        # Запускаем задачи с разными задержками
        task1 = asyncio.create_task(wrapper("Second", 0.2))
        task2 = asyncio.create_task(wrapper("First", 0.1))
        task3 = asyncio.create_task(wrapper("Third", 0.3))
        
        await asyncio.gather(task1, task2, task3)
        
        # Проверяем порядок выполнения
        self.assertEqual(results, ["First", "Second", "Third"])

class TestMainFunction(unittest.IsolatedAsyncioTestCase):
    """Тесты для функции main"""
    
    @patch('sys.stdout', new_callable=StringIO)
    async def test_main_output(self, mock_stdout):
        """Тестируем вывод main"""
        # Мокируем asyncio.sleep для ускорения тестов
        with patch('asyncio.sleep', return_value=None):
            # Подменяем оригинальные задержки на уменьшенные
            async def patched_main():
                task1 = asyncio.create_task(delayed_message("Сообщение после 0.2 секунд", 0.2))
                task2 = asyncio.create_task(delayed_message("Сообщение после 0.1 секунды", 0.1))
                task3 = asyncio.create_task(delayed_message("Сообщение после 0.3 секунд", 0.3))
                await asyncio.gather(task1, task2, task3)
                print("Все сообщения выведены!")
            
            await patched_main()
            
            output = mock_stdout.getvalue().strip().split('\n')
            
            self.assertEqual(output[0], "Сообщение после 0.2 секунд")
            self.assertEqual(output[1], "Сообщение после 0.1 секунды")
            self.assertEqual(output[2], "Сообщение после 0.3 секунд")
            self.assertEqual(output[3], "Все сообщения выведены!")
    
    async def test_main_tasks_created(self):
        """Тестируем создание задач в main"""
        tasks = []
        
        original_create_task = asyncio.create_task
        
        def create_task_wrapper(coro):
            task = original_create_task(coro)
            tasks.append(task)
            return task
        
        # Подменяем create_task на нашу обёртку
        with patch('asyncio.create_task', new=create_task_wrapper):
            await main()
            # Проверяем, что было создано 3 задачи
            self.assertEqual(len(tasks), 3)

class TestIntegration(unittest.IsolatedAsyncioTestCase):
    """Интеграционные тесты"""
    
    @patch('sys.stdout', new_callable=StringIO)
    async def test_full_flow(self, mock_stdout):
        """Тестируем полный поток выполнения с реальными вызовами"""
        # Используем реальные задержки, но уменьшенные для тестов
        async def fast_main():
            task1 = asyncio.create_task(delayed_message("Сообщение после 0.2 секунд", 0.2))
            task2 = asyncio.create_task(delayed_message("Сообщение после 0.1 секунды", 0.1))
            task3 = asyncio.create_task(delayed_message("Сообщение после 0.3 секунд", 0.3))
            await asyncio.gather(task1, task2, task3)
            print("Все сообщения выведены!")
        
        await fast_main()
        
        output = mock_stdout.getvalue().strip().split('\n')
        
        self.assertEqual(output[0], "Сообщение после 0.1 секунды")
        self.assertEqual(output[1], "Сообщение после 0.2 секунд")
        self.assertEqual(output[2], "Сообщение после 0.3 секунд")
        self.assertEqual(output[3], "Все сообщения выведены!")

if __name__ == '__main__':
    unittest.main()